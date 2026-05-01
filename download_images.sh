#!/usr/bin/env bash
# Usage: ./download_images.sh <URL> [output_dir]
# Downloads images from Pinterest boards and most image websites.
# Requires only: curl + python3 (no pip/installs needed)

set -euo pipefail

URL="${1:-}"
OUTDIR="${2:-.}"

if [[ -z "$URL" ]]; then
  echo "Usage: $0 <URL> [output_dir]"
  exit 1
fi

mkdir -p "$OUTDIR"

echo "Fetching page: $URL"
echo "Saving to: $OUTDIR"
echo ""

HTML=$(curl -s -L --max-time 30 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.5" \
  "$URL")

if [[ -z "$HTML" ]]; then
  echo "Error: failed to fetch page or page was empty."
  exit 1
fi

echo "Page fetched (${#HTML} bytes). Extracting image URLs..."

TMPFILE=$(mktemp /tmp/dl_images_XXXXXX.html)
trap 'rm -f "$TMPFILE"' EXIT
printf '%s' "$HTML" > "$TMPFILE"

IMAGE_URLS=$(python3 - "$URL" "$TMPFILE" <<'PYEOF'
import sys, re, json, html as htmlmod, urllib.parse

page_url = sys.argv[1]
with open(sys.argv[2], 'r', encoding='utf-8', errors='replace') as f:
    page = f.read()
base = urllib.parse.urlparse(page_url)

seen_hashes = {}   # hash -> best (priority, url)
generic_seen = set()

# Resolution priority for Pinterest CDN (higher = better)
RES_PRIORITY = {
    'originals': 100,
    '1200x': 90,
    '736x': 80,
    '600x': 70,
    '474x': 60,
    '236x': 30,
    '170x': 20,
    '75x75': 5,
}

def res_priority(url):
    for res, pri in RES_PRIORITY.items():
        if '/' + res + '/' in url:
            return pri
    return 1

# ── Pinterest: parse __PWS_INITIAL_PROPS__ JSON blob ──────────────────────────
m = re.search(r'<script[^>]+id="__PWS_INITIAL_PROPS__"[^>]*>(.*?)</script>', page, re.DOTALL)
if m:
    try:
        data = json.loads(m.group(1))

        def walk(obj):
            if isinstance(obj, str):
                if 'i.pinimg.com' in obj and re.search(r'\.(jpg|jpeg|png|gif|webp)$', obj, re.I):
                    # Extract the hash (filename without extension) as dedup key
                    fname = obj.rsplit('/', 1)[-1].rsplit('.', 1)[0]
                    pri = res_priority(obj)
                    if fname not in seen_hashes or pri > seen_hashes[fname][0]:
                        seen_hashes[fname] = (pri, obj)
            elif isinstance(obj, dict):
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(data)
    except Exception:
        pass

# ── Pinterest: also try __PWS_DATA__ ──────────────────────────────────────────
m2 = re.search(r'<script[^>]+id="__PWS_DATA__"[^>]*>(.*?)</script>', page, re.DOTALL)
if m2:
    try:
        data2 = json.loads(m2.group(1))
        walk(data2)
    except Exception:
        pass

# ── Generic: <img src>, srcset, background-image, JSON strings ───────────────
if not seen_hashes:
    patterns = [
        r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^"\']*)?)["\']',
        r'srcset=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))',
        r'"(https?://[^"\'<>\s]+\.(?:jpg|jpeg|png|gif|webp))"',
        r"'(https?://[^'\"<>\s]+\.(?:jpg|jpeg|png|gif|webp))'",
        r'url\(["\']?(https?://[^"\')<>\s]+\.(?:jpg|jpeg|png|gif|webp))["\']?\)',
    ]
    for pat in patterns:
        for m in re.finditer(pat, page, re.IGNORECASE):
            raw = htmlmod.unescape(m.group(1).strip())
            if raw.startswith('//'):
                raw = base.scheme + ':' + raw
            elif raw.startswith('/'):
                raw = base.scheme + '://' + base.netloc + raw
            if raw not in generic_seen:
                generic_seen.add(raw)

# ── Output ────────────────────────────────────────────────────────────────────
if seen_hashes:
    # For Pinterest: upgrade each URL to 736x if available, else use best found
    for _, (pri, url) in sorted(seen_hashes.items()):
        upgraded = re.sub(r'/(originals|1200x|736x|600x|474x|236x|170x|75x75_RS|75x75|60x60|45x45)/', '/736x/', url)
        print(upgraded)
else:
    for u in generic_seen:
        print(u)

PYEOF
)

if [[ -z "$IMAGE_URLS" ]]; then
  echo "No images found on the page."
  echo "Tip: Pinterest may require a logged-in session for some boards."
  exit 0
fi

COUNT=$(echo "$IMAGE_URLS" | grep -c .)
echo "Found $COUNT unique image(s). Downloading..."
echo ""

INDEX=0
DOWNLOADED=0
FAILED=0

while IFS= read -r IMG_URL; do
  [[ -z "$IMG_URL" ]] && continue
  INDEX=$((INDEX + 1))

  FILENAME=$(python3 -c "
import urllib.parse, os, sys
u = sys.argv[1]
path = urllib.parse.urlparse(u).path
name = os.path.basename(path).split('?')[0]
print(name or 'image_${INDEX}.jpg')
" "$IMG_URL")

  DEST="$OUTDIR/$FILENAME"
  BASE="${FILENAME%.*}"
  EXT="${FILENAME##*.}"
  N=1
  while [[ -e "$DEST" ]]; do
    DEST="$OUTDIR/${BASE}_${N}.${EXT}"
    N=$((N + 1))
  done

  printf "[%d/%d] %s ... " "$INDEX" "$COUNT" "$FILENAME"

  HTTP_CODE=$(curl -s -L --max-time 30 -w "%{http_code}" \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: $URL" \
    -o "$DEST" "$IMG_URL")

  SIZE=$(wc -c < "$DEST" 2>/dev/null || echo 0)

  if [[ "$HTTP_CODE" == "200" && "$SIZE" -gt 500 ]]; then
    echo "OK (${SIZE} bytes)"
    DOWNLOADED=$((DOWNLOADED + 1))
  else
    # Fall back to 474x if 736x wasn't available
    FALLBACK_URL=$(echo "$IMG_URL" | sed 's|/736x/|/474x/|')
    if [[ "$FALLBACK_URL" != "$IMG_URL" ]]; then
      HTTP_CODE2=$(curl -s -L --max-time 30 -w "%{http_code}" \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        -H "Referer: $URL" \
        -o "$DEST" "$FALLBACK_URL")
      SIZE2=$(wc -c < "$DEST" 2>/dev/null || echo 0)
      if [[ "$HTTP_CODE2" == "200" && "$SIZE2" -gt 500 ]]; then
        echo "OK 474x fallback (${SIZE2} bytes)"
        DOWNLOADED=$((DOWNLOADED + 1))
        continue
      fi
    fi
    echo "FAILED (HTTP $HTTP_CODE, ${SIZE} bytes)"
    rm -f "$DEST"
    FAILED=$((FAILED + 1))
  fi

done <<< "$IMAGE_URLS"

echo ""
echo "Done. Downloaded: $DOWNLOADED  Failed/skipped: $FAILED"
echo "Files saved to: $(realpath "$OUTDIR")"
