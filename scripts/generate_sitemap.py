#!/usr/bin/env python3
"""Generate sitemap.xml for the GitHub Pages site.

The site uses a static sitemap instead of the jekyll-sitemap plugin so that the
output can be validated locally and so scheduled lessons are clearly listed.

Usage:
    python scripts/generate_sitemap.py
    python scripts/generate_sitemap.py --check
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "_config.yml"
SITEMAP = ROOT / "sitemap.xml"

STATIC_PATHS = ["/", "/lessons/", "/docs/", "/resources/"]


def read_config() -> tuple[str, str]:
    text = CONFIG.read_text(encoding="utf-8")
    url = re.search(r"^url:\s*[\"']?([^\"'\n]+)", text, re.M)
    baseurl = re.search(r"^baseurl:\s*[\"']?([^\"'\n]*)", text, re.M)
    if not url:
        raise SystemExit("_config.yml is missing a url")
    base = (baseurl.group(1).strip() if baseurl else "").rstrip("/")
    if base and not base.startswith("/"):
        base = "/" + base
    return url.group(1).strip().rstrip("/"), base


def permalink_for(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    front = text[:end]
    match = re.search(r"^permalink:\s*[\"']?([^\"'\n]+)", front, re.M)
    if not match:
        return None
    permalink = match.group(1).strip()
    if not permalink.startswith("/"):
        permalink = "/" + permalink
    if not permalink.endswith("/") and "." not in permalink.rsplit("/", 1)[-1]:
        permalink += "/"
    return permalink


def collect_pages() -> list[tuple[str, str]]:
    """Return (permalink, source path) pairs for public HTML pages."""
    pages: dict[str, str] = {}
    for source in sorted(ROOT.glob("*.md")):
        if source.stem.lower() in {"readme", "license", "contributing", "code_of_conduct", "security", "changelog", "agents", "404"}:
            continue
        permalink = permalink_for(source) or "/"
        pages[permalink] = source.name
    for folder in ("docs", "resources", "lessons"):
        for source in sorted((ROOT / folder).glob("*.md")):
            permalink = permalink_for(source) or f"/{folder}/{source.stem}/"
            pages[permalink] = f"{folder}/{source.name}"
    for path in STATIC_PATHS:
        pages.setdefault(path, "index")
    return sorted(pages.items(), key=lambda item: (item[0] != "/", item[0]))


def build_sitemap() -> str:
    url, baseurl = read_config()
    metadata = json.loads((ROOT / "data" / "playlist-metadata.json").read_text(encoding="utf-8"))
    lastmod = metadata.get("extraction_date") or "2026-11-14"
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for permalink, source in collect_pages():
        loc = f"{url}{baseurl}{permalink}"
        priority = "1.0" if permalink == "/" else ("0.9" if permalink == "/lessons/" else "0.8")
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = build_sitemap()
    changed = not SITEMAP.exists() or SITEMAP.read_text(encoding="utf-8") != content
    if changed and not args.check:
        SITEMAP.write_text(content, encoding="utf-8", newline="\n")
    count = content.count("<loc>")
    if args.check and changed:
        print("sitemap.xml is out of date. Run: python scripts/generate_sitemap.py")
        return 1
    print(f"sitemap.xml: {count} URLs. " + ("Updated." if changed else "Up to date."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
