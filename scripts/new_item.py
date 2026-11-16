#!/usr/bin/env python3
"""Scaffold a new kit item from a template.

Usage:
  python scripts/new_item.py <skill|prompt|project|tool> <slug> "<Title>"

Example:
  python scripts/new_item.py skill integration-error-explainer "Integration Error Explainer"
"""
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = ("skill", "prompt", "project", "tool")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in TYPES:
        sys.exit(__doc__)
    kind, slug, title = sys.argv[1], sys.argv[2], sys.argv[3]
    if not SLUG.match(slug):
        sys.exit("Slug must be lowercase letters, digits and hyphens, e.g. integration-error-explainer")

    dest = ROOT / "kit" / f"{kind}s" / slug
    if dest.exists():
        sys.exit(f"{dest.relative_to(ROOT)} already exists")
    shutil.copytree(ROOT / "templates" / kind, dest)

    values = {"{{slug}}": slug, "{{title}}": title, "{{date}}": date.today().isoformat()}
    for f in dest.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".json", ".txt"}:
            text = f.read_text(encoding="utf-8")
            for key, value in values.items():
                text = text.replace(key, value)
            f.write_text(text, encoding="utf-8")

    print(f"Created {dest.relative_to(ROOT)}/")
    print("Next: write the content, fill the TODO fields in item.json, then run: python scripts/build.py")


if __name__ == "__main__":
    main()
