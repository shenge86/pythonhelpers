#!/usr/bin/env bash
# Downloads full-resolution images from gallery/thumbnail pages.
# Follows each thumbnail link, finds the full-res image, and downloads it.
# Requires only curl + python3 (no pip).
#
# Usage:
#   ./download_linked_images.sh [options] <URL>
#
# Options:
#   -o, --output <dir>       Output directory (default: current dir)
#   -d, --delay <secs>       Pause between requests (default: 0.5)
#   -f, --format <fmt>       Only save images of this format: jpg, png, gif,
#                            webp, or comma-separated list e.g. jpg,png
#   -m, --min-size <KB>      Skip images smaller than this size in KB (default: 0)
#   -h, --help               Show this help

set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────
URL=""
OUTDIR="."
DELAY="0.5"
FORMATS=""       # empty = accept all
MIN_KB=0

# ── Argument parsing ──────────────────────────────────────────────────────────
usage() {
  grep '^#' "$0" | grep -v '#!/' | sed 's/^# \?//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)    OUTDIR="$2";  shift 2 ;;
    -d|--delay)     DELAY="$2";   shift 2 ;;
    -f|--format)    FORMATS="$2"; shift 2 ;;
    -m|--min-size)  MIN_KB="$2";  shift 2 ;;
    -h|--help)      usage 0 ;;
    -*)             echo "Unknown option: $1"; usage 1 ;;
    *)              URL="$1"; shift ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo "Error: URL is required."
  usage 1
fi

# Normalise formats to lowercase, no dots, pipe-separated for grep -iE
FORMAT_GREP=""
if [[ -n "$FORMATS" ]]; then
  FORMAT_GREP=$(python3 -c "
import sys
fmts = [f.strip().lower().lstrip('.') for f in sys.argv[1].split(',')]
# jpg and jpeg are the same
expanded = []
for f in fmts:
    expanded.append(f)
    if f == 'jpg': expanded.append('jpeg')
    if f == 'jpeg': expanded.append('jpg')
print('|'.join(dict.fromkeys(expanded)))
" "$FORMATS")
fi

MIN_BYTES=$(( MIN_KB * 1024 ))

mkdir -p "$OUTDIR"

echo "Fetching gallery page: $URL"
[[ -n "$FORMAT_GREP" ]] && echo "Format filter: $FORMATS"
[[ "$MIN_KB" -gt 0 ]]   && echo "Min size: ${MIN_KB} KB"
echo "Saving to: $OUTDIR"
echo ""

TMPFILE=$(mktemp /tmp/dl_gallery_XXXXXX.html)
TMPPAGE=$(mktemp /tmp/dl_imgpage_XXXXXX.html)
trap 'rm -f "$TMPFILE" "$TMPPAGE"' EXIT

curl -s -L --max-time 30 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.5" \
  -o "$TMPFILE" "$URL"

if [[ ! -s "$TMPFILE" ]]; then
  echo "Error: failed to fetch page or page was empty."
  exit 1
fi

echo "Page fetched ($(wc -c < "$TMPFILE") bytes). Extracting thumbnail links..."

# ── Step 1: extract all href links associated with <img> tags ─────────────────
LINKS=$(python3 - "$URL" "$TMPFILE" <<'PYEOF'
import sys, re, html as htmlmod, urllib.parse

page_url = sys.argv[1]
with open(sys.argv[2], 'r', encoding='utf-8', errors='replace') as f:
    page = f.read()

base = urllib.parse.urlparse(page_url)

def abs_url(href):
    href = htmlmod.unescape(href.strip())
    if href.startswith('//'): return base.scheme + ':' + href
    if href.startswith('/'): return base.scheme + '://' + base.netloc + href
    if href.startswith('http'): return href
    base_path = base.path.rsplit('/', 1)[0] + '/'
    return base.scheme + '://' + base.netloc + base_path + href

IMAGE_EXT = re.compile(r'\.(jpg|jpeg|png|gif|webp|bmp|tiff?)(\?.*)?$', re.I)
seen = set()
results = []

# Strategy 1: <a href="..."><img ...></a>
for m in re.finditer(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', page, re.DOTALL | re.IGNORECASE):
    href, inner = m.group(1), m.group(2)
    if '<img' not in inner.lower():
        continue
    href = abs_url(href)
    if not href.startswith('http'):
        continue
    if href not in seen:
        seen.add(href)
        results.append(href)

# Strategy 2: direct links to image files
for m in re.finditer(r'href=["\']([^"\']+)["\']', page, re.IGNORECASE):
    href = abs_url(m.group(1))
    if IMAGE_EXT.search(href) and href not in seen:
        seen.add(href)
        results.append(href)

for r in results:
    print(r)
PYEOF
)

if [[ -z "$LINKS" ]]; then
  echo "No thumbnail links found on the page."
  exit 0
fi

TOTAL=$(echo "$LINKS" | grep -c .)
echo "Found $TOTAL link(s) to follow. Resolving full-resolution images..."
echo ""

INDEX=0
DOWNLOADED=0
FAILED=0
SKIPPED=0
IMAGE_EXT_RE='\.(jpg|jpeg|png|gif|webp|bmp|tiff?)(\?.*)?$'

while IFS= read -r LINK; do
  [[ -z "$LINK" ]] && continue
  INDEX=$((INDEX + 1))
  printf "[%d/%d] %s\n" "$INDEX" "$TOTAL" "$LINK"

  # ── Case A: link is already a direct image URL ─────────────────────────────
  if echo "$LINK" | grep -qiE "$IMAGE_EXT_RE"; then
    FULL_URL="$LINK"
  else
    # ── Case B: follow the link, find full-res image on that page ──────────────
    sleep "$DELAY"
    curl -s -L --max-time 30 \
      -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
      -H "Referer: $URL" \
      -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
      -o "$TMPPAGE" "$LINK" 2>/dev/null \
      || { echo "  -> FAILED (could not fetch link page)"; FAILED=$((FAILED+1)); continue; }

    FULL_URL=$(python3 - "$LINK" "$TMPPAGE" <<'PYEOF'
import sys, re, html as htmlmod, urllib.parse

page_url = sys.argv[1]
with open(sys.argv[2], 'r', encoding='utf-8', errors='replace') as f:
    page = f.read()

base = urllib.parse.urlparse(page_url)
IMAGE_EXT = re.compile(r'\.(jpg|jpeg|png|gif|webp|bmp|tiff?)(\?[^"\'<>\s]*)?$', re.I)

def abs_url(u):
    u = htmlmod.unescape(u.strip())
    if u.startswith('//'): return base.scheme + ':' + u
    if u.startswith('/'): return base.scheme + '://' + base.netloc + u
    if u.startswith('http'): return u
    return base.scheme + '://' + base.netloc + '/' + u.lstrip('/')

candidates = []

# 1. og:image
for m in re.finditer(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', page, re.I):
    candidates.append((100, abs_url(m.group(1))))
for m in re.finditer(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', page, re.I):
    candidates.append((100, abs_url(m.group(1))))

# 2. Direct <a href="image.jpg"> links
for m in re.finditer(r'href=["\']([^"\']+)["\']', page, re.I):
    u = abs_url(m.group(1))
    if IMAGE_EXT.search(u):
        candidates.append((80, u))

# 3. Largest <img> by declared dimensions
for m in re.finditer(r'<img([^>]+)>', page, re.I | re.DOTALL):
    attrs = m.group(1)
    src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', attrs, re.I)
    if not src_m:
        continue
    src = abs_url(src_m.group(1))
    if not IMAGE_EXT.search(src):
        continue
    w = int(re.search(r'\bwidth=["\']?(\d+)', attrs, re.I).group(1)) if re.search(r'\bwidth=["\']?(\d+)', attrs, re.I) else 0
    h = int(re.search(r'\bheight=["\']?(\d+)', attrs, re.I).group(1)) if re.search(r'\bheight=["\']?(\d+)', attrs, re.I) else 0
    candidates.append((10 + w + h, src))

# 4. srcset — highest width descriptor
for m in re.finditer(r'srcset=["\']([^"\']+)["\']', page, re.I):
    for part in m.group(1).split(','):
        tokens = part.strip().split()
        if not tokens: continue
        u = abs_url(tokens[0])
        if not IMAGE_EXT.search(u): continue
        try:
            val = float((tokens[1] if len(tokens) > 1 else '1x').rstrip('wx'))
        except Exception:
            val = 1.0
        candidates.append((50 + val, u))

# 5. Fallback: any image URL in page
for m in re.finditer(r'["\']( (?:https?://)[^"\'<>\s]+\.(?:jpg|jpeg|png|gif|webp))["\']', page, re.I):
    candidates.append((5, abs_url(m.group(1).strip())))

if not candidates:
    sys.exit(0)

seen = set()
for score, u in sorted(candidates, key=lambda x: -x[0]):
    if u not in seen:
        seen.add(u)
        print(u)
        break
PYEOF
    )

    if [[ -z "$FULL_URL" ]]; then
      echo "  -> could not find full-res image on page"
      FAILED=$((FAILED+1))
      continue
    fi
  fi

  # ── Format filter (check URL extension before downloading) ───────────────────
  if [[ -n "$FORMAT_GREP" ]]; then
    if ! echo "$FULL_URL" | grep -qiE "\.(${FORMAT_GREP})(\?|$)"; then
      echo "  -> skipped (format not in: $FORMATS)"
      SKIPPED=$((SKIPPED+1))
      continue
    fi
  fi

  printf "  -> %s\n" "$FULL_URL"

  # ── Download ──────────────────────────────────────────────────────────────────
  FILENAME=$(python3 -c "
import urllib.parse, os, sys
u = sys.argv[1]
path = urllib.parse.urlparse(u).path
name = os.path.basename(path).split('?')[0]
print(name if name else 'image_$INDEX.jpg')
" "$FULL_URL")

  DEST="$OUTDIR/$FILENAME"
  BASE="${FILENAME%.*}"
  EXT="${FILENAME##*.}"
  N=1
  while [[ -e "$DEST" ]]; do
    DEST="$OUTDIR/${BASE}_${N}.${EXT}"
    N=$((N+1))
  done

  HTTP_CODE=$(curl -s -L --max-time 60 -w "%{http_code}" \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -H "Referer: $LINK" \
    -o "$DEST" "$FULL_URL")

  SIZE=$(wc -c < "$DEST" 2>/dev/null || echo 0)

  # ── Min-size filter ───────────────────────────────────────────────────────────
  if [[ "$HTTP_CODE" == "200" && "$SIZE" -gt 500 ]]; then
    if [[ "$MIN_BYTES" -gt 0 && "$SIZE" -lt "$MIN_BYTES" ]]; then
      echo "  -> skipped ($(( SIZE / 1024 )) KB < min ${MIN_KB} KB)"
      rm -f "$DEST"
      SKIPPED=$((SKIPPED+1))
    else
      echo "  -> saved as $FILENAME ($(( SIZE / 1024 )) KB)"
      DOWNLOADED=$((DOWNLOADED+1))
    fi
  else
    echo "  -> FAILED (HTTP $HTTP_CODE, ${SIZE} bytes)"
    rm -f "$DEST"
    FAILED=$((FAILED+1))
  fi

  sleep "$DELAY"

done <<< "$LINKS"

echo ""
echo "Done. Downloaded: $DOWNLOADED  Skipped: $SKIPPED  Failed: $FAILED"
echo "Files saved to: $(realpath "$OUTDIR")"
