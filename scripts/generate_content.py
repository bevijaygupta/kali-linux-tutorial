#!/usr/bin/env python3
"""Generate machine-readable content: the lesson search index and llms.txt.

Usage:
    python scripts/generate_content.py
    python scripts/generate_content.py --check
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DATA = ROOT / "assets" / "data"
LLMS = ROOT / "llms.txt"

REPO_URL = "https://github.com/bevijaygupta/kali-linux-tutorial"
SITE_URL = "https://bevijaygupta.github.io/kali-linux-tutorial"
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLYDHfwsEk0RY"
CHANNEL_URL = "https://www.youtube.com/@EINITIAL24"

DOCS = [
    ("Getting started", "/docs/getting-started/", "How to use the course, prerequisites and the fastest path to your first lab."),
    ("Installation", "/docs/installation/", "Download Kali Linux safely, verify the ISO and install it in a virtual machine."),
    ("Lab setup", "/docs/lab-setup/", "Build an isolated, snapshot-backed lab for legal practice."),
    ("Linux fundamentals", "/docs/linux-fundamentals/", "Terminal basics, files, permissions, users and processes."),
    ("Networking basics", "/docs/networking-basics/", "IP addresses, ports, DNS, HTTP and how traffic moves."),
    ("Reconnaissance", "/docs/reconnaissance/", "Footprinting, OSINT, DNS enumeration and Nmap scanning."),
    ("Vulnerability analysis", "/docs/vulnerability-analysis/", "Searchsploit, Nikto, Lynis and reading scan results."),
    ("Exploitation basics", "/docs/exploitation-basics/", "Metasploit concepts and safe exploitation in a lab."),
    ("Password attacks", "/docs/password-attacks/", "Hashing, wordlists, offline cracking and online attacks."),
    ("Wireless security", "/docs/wireless-security/", "Wi-Fi security concepts, Aircrack-ng and defending your network."),
    ("Web application security", "/docs/web-application-security/", "XSS, SQL injection, Burp Suite and Wireshark."),
    ("Study roadmap", "/docs/study-roadmap/", "A week-by-week plan for finishing the course."),
]

RESOURCES = [
    ("Cheat sheet", "/resources/cheat-sheet/", "Safe command reference for the tools covered in the course."),
    ("Lab checklist", "/resources/lab-checklist/", "Pre-flight checks before every practice session."),
    ("Official links", "/resources/official-links/", "Vendor and project documentation, plus acceptable use rules."),
    ("Glossary", "/resources/glossary/", "Plain-language definitions of course terminology."),
]

MODULE_BLURBS = {
    1: "Why Kali exists, how to verify the ISO, and how to run it safely in VirtualBox or VMware.",
    2: "The terminal, file operations, permissions, users and the shortcuts that make Linux work.",
    3: "IP addresses, ports, DNS, Tor, VPNs, proxies and MAC addresses — with honest limits.",
    4: "Footprinting, OSINT, DNS enumeration and Nmap scanning against your own lab network.",
    5: "Nikto, Searchsploit, Lynis and web reconnaissance, then SQL injection tools in a safe lab.",
    6: "Hashing, wordlists, offline cracking and online password attacks — plus how to defend.",
    7: "Packet capture, ARP and DNS spoofing, and how to read traffic without breaking a network.",
    8: "Wi-Fi terminology, WEP and WPA/WPA2 testing, and practical wireless defense.",
    9: "Metasploit, buffer overflows, honeypots and browser exploitation concepts.",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def clean_title(raw: str) -> str:
    """Mirror the lesson generator so search results and pages agree."""
    import re

    parts = [part.strip() for part in raw.split("|")]
    kept = []
    for part in parts:
        if not part:
            continue
        if re.match(r"^(ch\.?|chapter)\s*\d+\b", part, re.I):
            continue
        if re.match(r"^\d{4}\b", part) and (len(part) <= 30 or re.fullmatch(r"\d{4}(\s+#\w+)*", part)):
            continue
        if part.startswith("#"):
            continue
        if re.search(r"\b(chapter|ch\.?)\s*\d+\b", part, re.I) and (
            "kali" in part.lower() or "course" in part.lower() or len(part) < 40
        ):
            continue
        kept.append(part)
    title = " | ".join(kept) if kept else raw
    title = re.sub(r"\s+#\w+", "", title)
    title = re.sub(r"\s+(ch\.?|chapter)\s*\d+\s*$", "", title, flags=re.I)
    return re.sub(r"\s+", " ", title).strip(" |-")


def build_course_data(playlist: dict, curricula: dict) -> dict:
    videos = playlist["videos"]
    modules: dict[str, list[dict]] = {}
    for video in sorted(videos, key=lambda item: int(item["chapter"])):
        name = (curricula.get(str(video["chapter"])) or {}).get("module") or video.get("module") or "Course"
        modules.setdefault(name, []).append(video)
    module_rows = []
    for name, items in modules.items():
        match = re.match(r"Module\s+(\d+)", name)
        number = int(match.group(1)) if match else len(module_rows) + 1
        chapters = sorted(int(item["chapter"]) for item in items)
        module_rows.append(
            {
                "number": number,
                "name": name,
                "blurb": MODULE_BLURBS.get(number, ""),
                "start": chapters[0],
                "end": chapters[-1],
                "count": len(chapters),
                "published": sum(1 for item in items if item.get("status") == "published"),
                "scheduled": sum(1 for item in items if item.get("status") == "scheduled"),
                "first_lesson": chapters[0],
                "url": f"/lessons/lesson-{chapters[0]:03d}/",
            }
        )
    module_rows.sort(key=lambda row: row["number"])
    metadata = load_json(DATA_DIR / "playlist-metadata.json")
    return {
        "total": metadata["total_videos"],
        "published": metadata["published_videos"],
        "scheduled": metadata["scheduled_videos"],
        "last_checked": metadata["extraction_date"],
        "modules": module_rows,
    }


def build_search_index(playlist: dict, curricula: dict) -> list[dict]:
    entries = []
    for video in sorted(playlist["videos"], key=lambda item: int(item["chapter"])):
        chapter = int(video["chapter"])
        curriculum = curricula.get(str(chapter), {})
        topic = clean_title(video["title"])
        search_bits = [topic, video.get("title", ""), curriculum.get("about", "")]
        search_bits.extend(curriculum.get("learn", []))
        search_bits.extend(concept.get("h", "") for concept in curriculum.get("concepts", []))
        entries.append(
            {
                "number": chapter,
                "chapter": chapter,
                "title": f"Chapter {chapter}: {topic}",
                "module": curriculum.get("module") or video.get("module"),
                "description": curriculum.get("seo_description") or "",
                "tags": curriculum.get("tags") or [],
                "url": f"/lessons/lesson-{chapter:03d}/",
                "video_url": video.get("url"),
                "status": video.get("status"),
                "duration": video.get("duration"),
                "published_date": video.get("published_date"),
                "text": " ".join(search_bits)[:1600],
            }
        )
    return entries


def build_llms(playlist: dict, curricula: dict, search_index: list[dict]) -> str:
    metadata = load_json(DATA_DIR / "playlist-metadata.json")
    published = metadata["published_videos"]
    scheduled = metadata["scheduled_videos"]
    lines = [
        "# Kali Linux Tutorials – EINITIAL24 Academy",
        "",
        "> A free, chapter-by-chapter Kali Linux course. This site adds written lesson notes, practical",
        "> checklists and official documentation links to the original YouTube playlist. Video content",
        "> belongs to EINITIAL24 ACADEMY and is linked, never re-hosted.",
        "",
        f"- Canonical site: {SITE_URL}/",
        f"- Source repository: {REPO_URL}",
        f"- YouTube playlist: {PLAYLIST_URL}",
        f"- Channel: {CHANNEL_URL}",
        f"- Chapters: {playlist['playlist']['total_videos']} ({published} published, {scheduled} scheduled)",
        f"- Metadata last checked: {metadata['extraction_date']}",
        "",
        "## How to use this site",
        "",
        "- Start with the [study roadmap](" + SITE_URL + "/docs/study-roadmap/).",
        "- Set up an isolated lab using the [lab checklist](" + SITE_URL + "/resources/lab-checklist/).",
        "- Follow lessons in chapter order; the YouTube playlist is newest-first.",
        "- Practice only on systems you own or have explicit written permission to test.",
        "",
        "## Documentation",
        "",
    ]
    for label, path, description in DOCS:
        lines.append(f"- [{label}]({SITE_URL}{path}): {description}")
    lines += ["", "## Resources", ""]
    for label, path, description in RESOURCES:
        lines.append(f"- [{label}]({SITE_URL}{path}): {description}")
    lines += ["", "## Lessons", ""]
    for entry in search_index:
        curriculum = curricula.get(str(entry["chapter"]), {})
        summary = curriculum.get("seo_description") or entry["description"]
        state = "published" if entry["status"] == "published" else "scheduled"
        lines.append(f"- [{entry['title']}]({SITE_URL}{entry['url']}): {summary} ({state})")
    lines += [
        "",
        "## Licensing",
        "",
        "- Written notes and site code: see LICENSE (MIT for code, CC BY 4.0 for written content).",
        "- Video titles, descriptions and thumbnails belong to EINITIAL24 ACADEMY.",
        "- No transcripts or video files are hosted in this repository.",
        "",
        "## Optional",
        "",
        f"- [README]({REPO_URL}#readme)",
        f"- [Contributing]({REPO_URL}/blob/main/CONTRIBUTING.md)",
        f"- [Security policy]({REPO_URL}/blob/main/SECURITY.md)",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files are current")
    args = parser.parse_args()

    playlist = load_json(DATA_DIR / "playlist.json")
    curricula = load_json(DATA_DIR / "curriculum.json")
    index = build_search_index(playlist, curricula)
    course = build_course_data(playlist, curricula)
    search_json = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    llms = build_llms(playlist, curricula, index)
    course_json = json.dumps(course, ensure_ascii=False, indent=2) + "\n"

    ASSETS_DATA.mkdir(parents=True, exist_ok=True)
    (ROOT / "_data").mkdir(exist_ok=True)
    targets = [
        (ASSETS_DATA / "lessons-index.json", search_json),
        (LLMS, llms),
        (ROOT / "_data" / "course.json", course_json),
    ]
    changed = []
    for path, content in targets:
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(content, encoding="utf-8", newline="\n")

    if args.check and changed:
        print("Generated content is out of date:")
        for item in changed:
            print(f"  - {item}")
        return 1
    print(f"Search index: {len(index)} lessons. " + ("Updated: " + ", ".join(changed) if changed else "Up to date."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
