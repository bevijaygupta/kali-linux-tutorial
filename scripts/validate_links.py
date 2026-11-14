#!/usr/bin/env python3
"""Validate repository data, generated pages, links and SEO metadata.

Checks performed:
  * every JSON file parses and playlist/curriculum keys agree;
  * all 76 lesson pages exist with required front matter and sections;
  * published vs scheduled metadata rules are respected;
  * internal links, Liquid relative_url paths and local assets resolve;
  * page titles and descriptions are unique;
  * the sitemap covers every public page;
  * legal/safety notices are present on lesson pages.

Usage:
    python scripts/validate_links.py
    python scripts/validate_links.py --strict   # treat warnings as errors
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
BASEURL = "/kali-linux-tutorial"
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "sitemap.xml",
    "robots.txt",
    "llms.txt",
    "404.md",
    "_config.yml",
    "index.md",
    "requirements.txt",
    ".gitignore",
    ".env.example",
    "package.json",
    "data/playlist.json",
    "data/playlist-metadata.json",
    "data/curriculum.json",
    "assets/data/lessons-index.json",
    "assets/css/main.css",
    "assets/js/theme.js",
    "assets/js/search.js",
    "assets/js/lesson.js",
    "assets/images/logo.svg",
    "docs/index.md",
    "docs/getting-started.md",
    "docs/installation.md",
    "docs/lab-setup.md",
    "docs/linux-fundamentals.md",
    "docs/networking-basics.md",
    "docs/reconnaissance.md",
    "docs/vulnerability-analysis.md",
    "docs/exploitation-basics.md",
    "docs/password-attacks.md",
    "docs/wireless-security.md",
    "docs/web-application-security.md",
    "docs/study-roadmap.md",
    "resources/index.md",
    "resources/cheat-sheet.md",
    "resources/lab-checklist.md",
    "resources/official-links.md",
    "resources/glossary.md",
    "lessons/index.md",
    "templates/lesson-template.md",
    "templates/docs-page-template.md",
    "templates/resource-template.md",
]
SECTION_HEADINGS = [
    "## Watch the tutorial",
    "## About this chapter",
    "## What you will learn",
    "## Important concepts",
    "## Practical notes",
    "## Related lessons",
    "## Additional resources",
    "## FAQ",
    "## Continue learning",
]
LESSON_FIELDS = [
    "layout", "title", "description", "permalink", "lesson_number", "total_lessons",
    "chapter", "module", "video_id", "video_url", "status", "playlist_position",
    "duration", "published_date",
]

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def parse_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict = {}
    for line in text[3:end].strip().splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        try:
            if raw.startswith(('"', "[", "{")):
                data[key.strip()] = json.loads(raw)
            elif raw in {"null", "~"}:
                data[key.strip()] = None
            elif raw.lower() in {"true", "false"}:
                data[key.strip()] = raw.lower() == "true"
            elif re.fullmatch(r"-?\d+", raw):
                data[key.strip()] = int(raw)
            else:
                data[key.strip()] = raw.strip("'")
        except json.JSONDecodeError:
            data[key.strip()] = raw
    return data


def normalize(path: str) -> str:
    path = unquote(path.split("#", 1)[0].split("?", 1)[0])
    if path.startswith(BASEURL):
        path = path[len(BASEURL):] or "/"
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return path


def site_path_exists(normalized: str, permalinks: dict[str, Path]) -> bool:
    """Resolve a site-absolute path to a page, static file or generated feed."""
    if normalized in permalinks:
        return True
    if normalized == "/feed.xml":
        return True
    candidate = ROOT / normalized.lstrip("/")
    return candidate.is_file() or (candidate.is_dir() and (candidate / "index.md").exists())


def collect_permalinks() -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for path in list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md")) + list((ROOT / "resources").glob("*.md")) + list((ROOT / "lessons").glob("*.md")):
        front = parse_front_matter(path)
        permalink = front.get("permalink")
        if permalink:
            pages[normalize(permalink)] = path
    return pages


def check_json() -> tuple[dict, dict]:
    playlist = curriculum = {}
    for path in sorted(ROOT.rglob("*.json")):
        if "_site" in path.parts or "node_modules" in path.parts or ".git" in path.parts:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            error(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
            continue
        if path.name == "playlist.json":
            playlist = data
        elif path.name == "curriculum.json":
            curriculum = data
    if playlist:
        videos = playlist.get("videos", [])
        chapters = [int(v["chapter"]) for v in videos if v.get("chapter")]
        expected_count = len(videos)
        if sorted(chapters) != list(range(1, expected_count + 1)):
            error(f"playlist.json: chapters are not exactly 1..{expected_count}")
        if len(set(chapters)) != len(chapters):
            error("playlist.json: duplicate chapter numbers")
        positions = sorted(int(v["position"]) for v in videos)
        if positions != list(range(1, len(videos) + 1)):
            error("playlist.json: playlist positions are not 1..N without gaps")
        for video in videos:
            vid = video.get("video_id")
            if not vid or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
                error(f"playlist.json: invalid video_id for chapter {video.get('chapter')}")
            if video.get("url") != f"https://www.youtube.com/watch?v={vid}":
                error(f"playlist.json: URL mismatch for chapter {video.get('chapter')}")
            if not video.get("title"):
                error(f"playlist.json: missing title for chapter {video.get('chapter')}")
            if video.get("status") == "scheduled":
                if video.get("published_date") or video.get("duration"):
                    error(f"playlist.json: scheduled chapter {video.get('chapter')} has a date or duration")
            elif video.get("status") == "published":
                if not video.get("published_date"):
                    error(f"playlist.json: published chapter {video.get('chapter')} has no date")
    if curriculum:
        expected = {str(chapter) for chapter in range(1, len(playlist.get("videos", [])) + 1)}
        if playlist:
            missing = expected - set(curriculum)
            orphaned = set(curriculum) - expected
            drafts = ROOT / "data" / "curriculum-drafts.json"
            if missing and drafts.exists():
                warn(
                    "curriculum.json: metadata-only chapters use drafts from "
                    f"data/curriculum-drafts.json: {', '.join(sorted(missing, key=int))}"
                )
            elif missing:
                error(
                    "curriculum.json: missing chapters "
                    f"{', '.join(sorted(missing, key=int))}; author notes or create drafts first"
                )
            if orphaned:
                error(f"curriculum.json: keys without videos: {', '.join(sorted(orphaned, key=int))}")
        for key, entry in curriculum.items():
            for field in ("module", "about", "learn", "concepts", "practical", "faq", "tags", "seo_title", "seo_description"):
                if field not in entry or entry[field] in ("", [], None):
                    error(f"curriculum.json[{key}]: missing or empty '{field}'")
            if entry.get("practical") and "safety" not in entry["practical"]:
                error(f"curriculum.json[{key}]: practical notes have no safety statement")
            if entry.get("seo_description") and len(entry["seo_description"]) > 175:
                warn(f"curriculum.json[{key}]: SEO description is {len(entry['seo_description'])} characters")
    return playlist, curriculum


def check_readme() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in ("<!-- CURRICULUM:START -->", "<!-- CURRICULUM:END -->"):
        if marker not in text:
            error("README.md: missing curriculum marker")
    rows = len(re.findall(r"^\| \[Lesson \d+\]", text, re.M))
    playlist = json.loads((ROOT / "data" / "playlist.json").read_text(encoding="utf-8"))
    expected_rows = len(playlist.get("videos", []))
    if rows != expected_rows:
        error(f"README.md: expected {expected_rows} curriculum rows, found {rows}")
    for heading in ("## About", "## Learning outcomes", "## Curriculum", "## FAQ"):
        if heading not in text:
            error(f"README.md: missing section '{heading}'")
    faq_count = len(re.findall(r"^### .+\?$", text.split("## FAQ", 1)[-1], re.M))
    if faq_count < 10:
        error(f"README.md: expected at least 10 FAQ questions, found {faq_count}")


def check_lessons(playlist: dict, curriculum: dict) -> None:
    videos = {int(v["chapter"]): v for v in playlist.get("videos", [])}
    paths = sorted((ROOT / "lessons").glob("lesson-*.md"))
    expected_lessons = len(videos)
    if len(paths) != expected_lessons:
        error(f"lessons: expected {expected_lessons} pages, found {len(paths)}")
    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        front = parse_front_matter(path)
        for field in LESSON_FIELDS:
            if field not in front:
                error(f"{rel}: missing front matter '{field}'")
        chapter = front.get("chapter")
        if not isinstance(chapter, int) or chapter not in videos:
            error(f"{rel}: chapter does not match playlist.json")
            continue
        if front.get("total_lessons") != expected_lessons:
            error(f"{rel}: total_lessons must be {expected_lessons}")
        video = videos[chapter]
        if front.get("video_id") != video["video_id"]:
            error(f"{rel}: video_id does not match playlist.json")
        if front.get("status") != video["status"]:
            error(f"{rel}: status does not match playlist.json")
        if front.get("title") in titles:
            error(f"{rel}: duplicate title with {titles[front['title']]}")
        titles[front.get("title", "")] = rel
        if front.get("description") in descriptions:
            error(f"{rel}: duplicate description with {descriptions[front.get('description', '')]}")
        descriptions[front.get("description", "")] = rel
        if not front.get("title") or len(str(front["title"])) < 20:
            error(f"{rel}: title too short for SEO")
        if not front.get("description") or not 70 <= len(str(front["description"])) <= 180:
            warn(f"{rel}: description length is {len(str(front.get('description', '')))}")
        for heading in SECTION_HEADINGS:
            if heading not in text:
                error(f"{rel}: missing section '{heading}'")
        if "Authorized learning only" not in text:
            error(f"{rel}: missing authorized-use notice")
        if "Before you run anything" not in text:
            error(f"{rel}: missing destructive-command warning")
        if video["status"] == "published":
            if f"youtube.com/watch?v={video['video_id']}" not in text:
                error(f"{rel}: missing original YouTube link")
            if "data-video-id" not in text:
                error(f"{rel}: missing lazy video player")
        else:
            if "Scheduled chapter" not in text:
                error(f"{rel}: scheduled lesson is not labelled")
            if "published_date: null" not in text or "duration: null" not in text:
                error(f"{rel}: scheduled lesson must have null date and duration")
            if "not on video footage" not in text:
                error(f"{rel}: scheduled lesson must disclose its sources")



def check_links(permalinks: dict[str, Path]) -> None:
    liquid_re = re.compile(r"\{\{\s*['\"]([^'\"]+)['\"]\s*\|\s*(?:relative_url|absolute_url)\s*\}\}")
    md_link_re = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
    html_link_re = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
    files = list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md")) + list((ROOT / "resources").glob("*.md")) + list((ROOT / "lessons").glob("*.md")) + list((ROOT / "_includes").glob("*.html")) + list((ROOT / "_layouts").glob("*.html"))

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        targets: list[tuple[str, str]] = []
        targets += [(m, "liquid") for m in liquid_re.findall(text)]
        for match in md_link_re.findall(text):
            if match.startswith(("http://", "https://", "mailto:", "#", "{{", "<")):
                continue
            targets.append((match, "markdown"))
        for match in html_link_re.findall(text):
            if match.startswith(("http://", "https://", "mailto:", "#", "{{", "data:")):
                continue
            targets.append((match, "html"))

        for target, kind in targets:
            target = target.strip()
            if not target or target.startswith("//"):
                continue
            if kind in {"markdown", "html"} and target.startswith("/"):
                # Root-absolute links break on GitHub Pages project sites, where
                # the site is served from /<repository>/. Use a Liquid filter.
                error(f"{rel}: root-absolute link '{target}' must use relative_url")
            if target.endswith(".md"):
                candidate = (path.parent / target).resolve()
                if not candidate.exists():
                    error(f"{rel}: broken markdown link '{target}'")
                continue
            if kind in {"liquid", "html"}:
                normalized = normalize(target)
                if normalized.startswith("/assets/"):
                    if not (ROOT / normalized.lstrip("/")).exists():
                        error(f"{rel}: missing asset '{target}'")
                elif not site_path_exists(normalized, permalinks):
                    error(f"{rel}: unresolved site path '{target}'")
                continue
            # Relative or root-relative markdown link.
            if target.startswith("/") or target.startswith(BASEURL + "/"):
                normalized = normalize(target)
                if normalized.startswith("/assets/"):
                    if not (ROOT / normalized.lstrip("/")).exists():
                        error(f"{rel}: missing asset '{target}'")
                elif not site_path_exists(normalized, permalinks):
                    error(f"{rel}: broken internal link '{target}'")
                continue
            candidate = (path.parent / target).resolve()
            if candidate.is_dir():
                index = candidate / "index.md"
                if not index.exists():
                    error(f"{rel}: directory link '{target}' has no index.md")
            elif not candidate.exists():
                warn(f"{rel}: relative link '{target}' is not a file in this repo")


def check_sitemap() -> None:
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    if len(locs) != len(set(locs)):
        error("sitemap.xml: duplicate URLs")
    playlist = json.loads((ROOT / "data" / "playlist.json").read_text(encoding="utf-8"))
    for chapter in range(1, len(playlist.get("videos", [])) + 1):
        if f"/lessons/lesson-{chapter:03d}/" not in sitemap:
            error(f"sitemap.xml: missing lesson-{chapter:03d}")
    if "404" in sitemap:
        error("sitemap.xml: 404 page must not be indexed")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "sitemap.xml" not in robots:
        error("robots.txt: does not reference the sitemap")


def check_required() -> None:
    for item in REQUIRED_FILES:
        if not (ROOT / item).exists():
            error(f"missing required file: {item}")
    for workflow in ("update-playlist.yml", "validate.yml", "pages.yml"):
        if not (ROOT / ".github" / "workflows" / workflow).exists():
            error(f"missing workflow: .github/workflows/{workflow}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="fail on warnings too")
    args = parser.parse_args()

    playlist, curriculum = check_json()
    check_required()
    check_readme()
    if playlist and curriculum:
        check_lessons(playlist, curriculum)
    permalinks = collect_permalinks()
    check_links(permalinks)
    if (ROOT / "sitemap.xml").exists():
        check_sitemap()

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
    if errors or (args.strict and warnings):
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
