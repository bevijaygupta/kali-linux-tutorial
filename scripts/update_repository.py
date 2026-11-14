#!/usr/bin/env python3
"""Run the full playlist update pipeline locally or in GitHub Actions.

Steps:
  1. Refresh data/playlist.json and data/playlist-metadata.json.
  2. Identify chapters that have no authored curriculum entry yet and write a
     clearly-labelled metadata-only draft file for a maintainer to review.
  3. Regenerate lesson pages, the search index, llms.txt and sitemap.xml.
  4. Validate the result.

The optional ``--enrich`` flag uses OPENAI_API_KEY or GEMINI_API_KEY to summarize
only the *official YouTube description* for new chapters. Those summaries are
written to data/curriculum-drafts.json with review_required=true; they are never
published automatically and the script never invents commands or transcripts.
Without a key the pipeline still succeeds with metadata-only output.

Usage:
    python scripts/update_repository.py
    python scripts/update_repository.py --skip-fetch
    python scripts/update_repository.py --enrich --strict
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DRAFTS = DATA_DIR / "curriculum-drafts.json"


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Load simple KEY=VALUE pairs from .env without replacing real env vars.

    Keeps the repository dependency-free while making ``cp .env.example .env``
    behave as documented. Values already exported in the environment win.
    """
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export "):].strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def run(script: str, *args: str) -> int:
    command = [sys.executable, str(ROOT / "scripts" / script), *args]
    print(f"\n$ {' '.join(command)}")
    return subprocess.call(command, cwd=ROOT)


def clean_title(raw: str) -> str:
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
    return re.sub(r"\s+(ch\.?|chapter)\s*\d+\s*$", "", title, flags=re.I).strip(" |-")


def excerpt(text: str, limit: int = 500) -> str:
    blocks = [re.sub(r"\s+", " ", block).strip() for block in re.split(r"\n\s*\n", text or "")]
    useful = [block for block in blocks if len(block) > 80 and not re.match(r"^(chapter \d+ of our|subscribe|disclaimer)", block, re.I)]
    text = useful[0] if useful else (blocks[0] if blocks else "")
    return text[:limit].rsplit(" ", 1)[0] + "…" if len(text) > limit else text


def llm_summary(description: str, title: str) -> tuple[str | None, str | None]:
    """Return (summary, provider). Summaries are drafts only."""
    prompt = (
        "You summarize official YouTube course descriptions. Use ONLY the supplied text. "
        "Do not add tools, commands, URLs, dates, claims or advice that are not present. "
        "Return two plain sentences, at most 70 words, neutral encyclopedic tone, no markdown. "
        "This is for a cybersecurity course that teaches authorized testing only.\n\n"
        f"Title: {title}\nDescription:\n{description[:6000]}"
    )
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if openai_key:
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        body = json.dumps(
            {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": 160}
        ).encode()
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"},
            method="POST",
        )
        provider = f"openai:{model}"
    elif gemini_key:
        model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        body = json.dumps(
            {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2, "maxOutputTokens": 200}}
        ).encode()
        request = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        provider = f"gemini:{model}"
    else:
        return None, None
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        print(f"warning: LLM enrichment failed ({exc}); continuing metadata-only")
        return None, provider
    try:
        if provider.startswith("openai"):
            text = payload["choices"][0]["message"]["content"]
        else:
            text = payload["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        print(f"warning: unexpected response from {provider}; continuing metadata-only")
        return None, provider
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:600], provider) if text else (None, provider)


def build_drafts(playlist: dict, curriculum: dict, enrich: bool) -> dict | None:
    videos = sorted(playlist["videos"], key=lambda item: int(item["chapter"]))
    missing = [video for video in videos if str(video["chapter"]) not in curriculum]
    if not missing:
        return None
    chapters: dict[str, dict] = {}
    for video in missing:
        chapter = int(video["chapter"])
        summary, provider = (llm_summary(video.get("description", ""), video.get("title", "")) if enrich else (None, None))
        draft = {
            "chapter": chapter,
            "title": clean_title(video.get("title", "")),
            "module": video.get("module"),
            "official_description_excerpt": excerpt(video.get("description", "")),
            "about": summary or "",
            "learn": [],
            "concepts": [],
            "practical": {"intro": "", "commands": [], "safety": ""},
            "faq": [],
            "tags": [],
            "seo_title": "",
            "seo_description": "",
            "review_required": True,
            "ai_assisted": bool(summary),
            "ai_provider": provider,
            "published_date": video.get("published_date"),
            "status": video.get("status"),
            "note": (
                "Draft only. The about text may be an AI summary of the official description and must be "
                "reviewed. Commands, concepts and FAQs must be authored by a human and verified in a lab."
                if summary
                else "Metadata-only draft. Author the lesson notes from the official video, then move this entry into data/curriculum.json."
            ),
        }
        chapters[str(chapter)] = draft
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "status": "needs_authoring",
        "chapters": chapters,
    }


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skip-fetch", action="store_true", help="use existing data/playlist.json")
    parser.add_argument("--enrich", action="store_true", help="draft summaries with OPENAI_API_KEY or GEMINI_API_KEY")
    parser.add_argument("--strict", action="store_true", help="pass --strict to validation")
    args = parser.parse_args()

    if not args.skip_fetch:
        code = run("fetch_playlist.py")
        if code != 0:
            print("Playlist refresh failed. Existing data was not replaced.")
            return code

    playlist = load_json(DATA_DIR / "playlist.json")
    curriculum = load_json(DATA_DIR / "curriculum.json")
    metadata = load_json(DATA_DIR / "playlist-metadata.json")

    drafts = build_drafts(playlist, curriculum, args.enrich)
    if drafts:
        DRAFTS.write_text(json.dumps(drafts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nNew chapters need authored notes: {', '.join(sorted(drafts['chapters'], key=int))}")
        print(f"Wrote {DRAFTS.relative_to(ROOT)} (review required, never published automatically).")
    elif DRAFTS.exists():
        DRAFTS.unlink()
        print("\nAll chapters have authored curriculum entries; removed the old drafts file.")

    for script in ("generate_lesson_pages.py", "generate_content.py", "generate_sitemap.py"):
        code = run(script)
        if code != 0:
            return code

    code = run("validate_links.py", *(["--strict"] if args.strict else []))
    if code != 0:
        print("\nValidation failed. Review the errors above before opening a pull request.")
        return code

    key_state = {
        "youtube_api": "available" if os.environ.get("YOUTUBE_API_KEY") else "not set (public-page fallback)",
        "openai": "available" if os.environ.get("OPENAI_API_KEY") else "not set",
        "gemini": "available" if os.environ.get("GEMINI_API_KEY") else "not set",
    }
    print("\nUpdate summary")
    print(f"  Source: {metadata.get('extraction_source')} ({metadata.get('extraction_date')})")
    print(f"  Videos: {metadata.get('total_videos')} total / {metadata.get('published_videos')} published / {metadata.get('scheduled_videos')} scheduled")
    print(f"  Chapters needing notes: {len(drafts['chapters']) if drafts else 0}")
    print(f"  YouTube API key: {key_state['youtube_api']}")
    print(f"  OPENAI_API_KEY: {key_state['openai']} · GEMINI_API_KEY: {key_state['gemini']}")
    if drafts:
        print("  Lesson pages for new chapters are metadata-only until curriculum.json is authored.")
    if not (os.environ.get("YOUTUBE_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        print("  No optional credentials present: metadata-only fallback used. This is an expected, supported mode.")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write("### Playlist update\n\n")
            handle.write(f"- Videos: **{metadata.get('total_videos')}** ({metadata.get('published_videos')} published, {metadata.get('scheduled_videos')} scheduled)\n")
            handle.write(f"- Extraction source: `{metadata.get('extraction_source')}`\n")
            handle.write(f"- Chapters needing authored notes: **{len(drafts['chapters']) if drafts else 0}**\n")
            handle.write(f"- YouTube API key: {key_state['youtube_api']}\n")
            handle.write(f"- OpenAI/Gemini keys: {key_state['openai']} / {key_state['gemini']}\n")
            if drafts:
                handle.write("- Action: review `data/curriculum-drafts.json`, author `data/curriculum.json`, then regenerate.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
