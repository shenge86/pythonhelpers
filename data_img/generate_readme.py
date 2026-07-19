#!/usr/bin/env python3
"""Regenerate data_img/README.md: a gallery of every image in this folder.

Run this after adding/removing images or subfolders in data_img.
"""
import argparse
import re
from pathlib import Path
from urllib.parse import quote

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}
IGNORE_DIR_NAME = "ignore"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def find_images(folder: Path) -> list[Path]:
    images = []
    for path in sorted(folder.rglob("*"), key=lambda p: p.as_posix()):
        if not is_image(path):
            continue
        rel_parents = {p.name.lower() for p in path.relative_to(folder).parents}
        if IGNORE_DIR_NAME in rel_parents:
            continue
        images.append(path)
    return images


def img_tag(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    src = quote(rel)
    label = path.stem
    return f'<img src="{src}" width="150" alt="{label}" title="{label}">'


def build_sections(root: Path) -> list[tuple[str, str, list[Path]]]:
    sections = []

    loose_images = sorted(
        (p for p in root.iterdir() if is_image(p)), key=lambda p: p.name
    )
    if loose_images:
        sections.append(("Loose images", "loose-images", loose_images))

    subfolders = sorted(
        (p for p in root.iterdir() if p.is_dir() and p.name.lower() != IGNORE_DIR_NAME),
        key=lambda p: p.name,
    )
    for sub in subfolders:
        images = find_images(sub)
        if images:
            sections.append((sub.name, slugify(sub.name), images))

    return sections


def build_readme(root: Path) -> str:
    sections = build_sections(root)
    total = sum(len(images) for _, _, images in sections)

    lines = [
        "# data_img Gallery",
        "",
        "Auto-generated gallery of every image in this folder, grouped by subfolder. "
        "Images inside any `ignore/` subfolder are excluded.",
        "",
        "## Contents",
        "",
    ]
    for title, anchor, images in sections:
        lines.append(f"- [{title}](#{anchor}) ({len(images)})")
    lines.append("")
    lines.append(f"**Total images: {total}**")

    for title, anchor, images in sections:
        lines.append("")
        lines.append(f'<a id="{anchor}"></a>')
        lines.append(f"## {title}")
        lines.append("")
        for image in images:
            lines.append(img_tag(image, root))
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default=Path(__file__).resolve().parent,
        type=Path,
        help="data_img folder to scan (defaults to the folder this script lives in)",
    )
    args = parser.parse_args()

    root = args.dir.resolve()
    readme_path = root / "README.md"
    readme_path.write_text(build_readme(root), encoding="utf-8", newline="\n")
    print(f"Wrote {readme_path}")


if __name__ == "__main__":
    main()
