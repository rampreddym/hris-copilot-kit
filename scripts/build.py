#!/usr/bin/env python3
"""Validate kit items, package downloads, and regenerate catalog.json and the README catalog.

Usage:
  python scripts/build.py                        # validate, build dist/, refresh catalog.json and README
  python scripts/build.py --check                # validate only; fail if catalog.json or README is stale
  python scripts/build.py --version v2026.11.0   # also stamp the release version into dist/catalog.json
"""
import argparse
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "kit"
DIST = ROOT / "dist"
README = ROOT / "README.md"
CATALOG = ROOT / "catalog.json"
CONFIG = json.loads((ROOT / "kit.config.json").read_text(encoding="utf-8"))

TYPES = {"skills": "skill", "prompts": "prompt", "projects": "project", "tools": "tool"}
TYPE_LABELS = {"skill": "Skill", "prompt": "Prompt card", "project": "Project template", "tool": "Tool"}
MAIN_FILE = {"skill": "SKILL.md", "prompt": "prompt.md", "project": "instructions.md", "tool": "README.md"}
REQUIRED = ["slug", "title", "type", "version", "summary", "platforms",
            "category", "added", "data_safety", "newsletter"]
SKILL_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXCLUDE = {"item.json", ".DS_Store", ".gitkeep"}
BEGIN, END = "<!-- catalog:start -->", "<!-- catalog:end -->"


def frontmatter(text):
    """Return top-level keys of a YAML frontmatter block, or None if there is none."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def validate_item(folder, type_name, errors):
    where = folder.relative_to(ROOT).as_posix()
    meta_path = folder / "item.json"
    if not meta_path.exists():
        errors.append(f"{where}: missing item.json")
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{where}/item.json: invalid JSON ({e})")
        return None

    missing = [k for k in REQUIRED if k not in meta]
    if missing:
        errors.append(f"{where}: item.json is missing {', '.join(missing)}")
        return None

    before = len(errors)
    if meta["slug"] != folder.name:
        errors.append(f"{where}: slug '{meta['slug']}' must match folder name '{folder.name}'")
    if not SLUG.match(meta["slug"]):
        errors.append(f"{where}: slug must be lowercase letters, digits and hyphens")
    if meta["type"] != type_name:
        errors.append(f"{where}: type '{meta['type']}' must be '{type_name}' for this folder")
    if not SEMVER.match(str(meta["version"])):
        errors.append(f"{where}: version must look like 1.0.0")
    if not isinstance(meta["platforms"], list) or not meta["platforms"]:
        errors.append(f"{where}: platforms must be a non-empty list")
    if not DATE.match(str(meta["added"])):
        errors.append(f"{where}: added must be a YYYY-MM-DD date")
    if not isinstance(meta["newsletter"], dict) or not {"title", "url"} <= set(meta["newsletter"]):
        errors.append(f"{where}: newsletter must be an object with title and url")
    for field in ("title", "summary", "category", "data_safety"):
        if not str(meta[field]).strip() or "{{" in str(meta[field]) or "TODO" in str(meta[field]):
            errors.append(f"{where}: fill in '{field}'")

    main = folder / MAIN_FILE.get(type_name, "README.md")
    if not main.exists():
        errors.append(f"{where}: missing {main.name}")
    elif type_name == "skill":
        fm = frontmatter(main.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{where}/SKILL.md: needs a --- frontmatter block with name and description")
        else:
            if fm.get("name") != folder.name:
                errors.append(f"{where}/SKILL.md: name must be '{folder.name}'")
            desc = fm.get("description", "")
            if not desc:
                errors.append(f"{where}/SKILL.md: description is required")
            elif len(desc) > 1024:
                errors.append(f"{where}/SKILL.md: description is {len(desc)} characters (max 1024)")
            extra = set(fm) - SKILL_KEYS
            if extra:
                errors.append(f"{where}/SKILL.md: unsupported frontmatter keys {sorted(extra)}; "
                              "put kit metadata in item.json")

    if len(errors) > before:
        return None
    meta["_dir"] = folder
    return meta


def load_items(errors):
    items, seen = [], set()
    for type_dir, type_name in TYPES.items():
        base = KIT / type_dir
        if not base.is_dir():
            continue
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            meta = validate_item(folder, type_name, errors)
            if meta is None:
                continue
            if meta["slug"] in seen:
                errors.append(f"{folder.relative_to(ROOT)}: slug '{meta['slug']}' is used twice")
                continue
            seen.add(meta["slug"])
            items.append(meta)
    items.sort(key=lambda i: (i["added"], i["slug"]), reverse=True)
    return items


def build_catalog(items):
    download = f"https://github.com/{CONFIG['repo']}/releases/latest/download"
    entries = []
    for item in items:
        entry = {k: v for k, v in item.items() if not k.startswith("_")}
        entry["path"] = item["_dir"].relative_to(ROOT).as_posix()
        entry["download"] = f"{download}/{item['slug']}.zip"
        entries.append(entry)
    return {
        "name": CONFIG["name"],
        "repo": f"https://github.com/{CONFIG['repo']}",
        "site": CONFIG["site"],
        "full_kit_download": f"{download}/{CONFIG['slug']}.zip",
        "item_count": len(entries),
        "items": entries,
    }


def render_table(items):
    if not items:
        return "_No items yet._"
    rows = ["| Item | Type | Platforms | Introduced in | Download |",
            "|---|---|---|---|---|"]
    for item in items:
        path = item["_dir"].relative_to(ROOT).as_posix()
        news = item["newsletter"]
        issue = f"[{news['title']}]({news['url']})" if news.get("url") else "Coming soon"
        dl = (f"https://github.com/{CONFIG['repo']}/releases/latest/download/{item['slug']}.zip")
        rows.append(f"| **[{item['title']}]({path})**<br>{item['summary']} "
                    f"| {TYPE_LABELS[item['type']]} | {', '.join(item['platforms'])} "
                    f"| {issue} | [zip]({dl}) |")
    return "\n".join(rows)


def render_readme(items):
    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        sys.exit(f"README.md must contain {BEGIN} and {END}")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n{render_table(items)}\n{END}{tail}"


def add_folder(zf, folder, arc_root):
    for f in sorted(folder.rglob("*")):
        if f.is_file() and f.name not in EXCLUDE and "__pycache__" not in f.parts:
            zf.write(f, f"{arc_root}/{f.relative_to(folder).as_posix()}")


def build_dist(items, catalog, version):
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for item in items:
        with zipfile.ZipFile(DIST / f"{item['slug']}.zip", "w", zipfile.ZIP_DEFLATED) as zf:
            add_folder(zf, item["_dir"], item["slug"])
    with zipfile.ZipFile(DIST / f"{CONFIG['slug']}.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for item in items:
            add_folder(zf, item["_dir"], f"{CONFIG['slug']}/{item['_dir'].relative_to(ROOT).as_posix()}")
        for name in ("README.md", "LICENSE", "CHANGELOG.md"):
            zf.write(ROOT / name, f"{CONFIG['slug']}/{name}")
    released = dict(catalog, version=version,
                    released_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    (DIST / "catalog.json").write_text(json.dumps(released, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only and fail if generated files are stale")
    parser.add_argument("--version", default="unreleased", help="release tag to stamp into dist/catalog.json")
    args = parser.parse_args()

    errors = []
    items = load_items(errors)
    if errors:
        print("Validation failed:", *[f"  - {e}" for e in errors], sep="\n")
        sys.exit(1)

    catalog = build_catalog(items)
    catalog_text = json.dumps(catalog, indent=2) + "\n"
    readme_text = render_readme(items)

    if args.check:
        stale = []
        if not CATALOG.exists() or CATALOG.read_text(encoding="utf-8") != catalog_text:
            stale.append("catalog.json")
        if README.read_text(encoding="utf-8") != readme_text:
            stale.append("README.md")
        if stale:
            print(f"Out of date: {', '.join(stale)}. Run: python scripts/build.py")
            sys.exit(1)
        print(f"OK: {len(items)} items valid, catalog and README up to date.")
        return

    CATALOG.write_text(catalog_text, encoding="utf-8")
    README.write_text(readme_text, encoding="utf-8")
    build_dist(items, catalog, args.version)
    print(f"Built {len(items)} items into dist/ ({args.version}); catalog.json and README refreshed.")
    for f in sorted(DIST.iterdir()):
        print(f"  {f.name:40} {f.stat().st_size:>8,} bytes")


if __name__ == "__main__":
    main()
