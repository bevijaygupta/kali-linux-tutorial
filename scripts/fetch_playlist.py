#!/usr/bin/env python3
"""Fetch metadata for a public YouTube playlist and write the repository data files.

Two data sources are supported:

1. YouTube Data API v3 (preferred) when YOUTUBE_API_KEY / --api-key is available.
2. Public playlist and watch pages, parsed from YouTube's `ytInitialData` and
   `ytInitialPlayerResponse` payloads (no key required, best effort).

The script never invents metadata. Values that cannot be verified are stored as
``null`` and the record is flagged with ``metadata_status``.

Usage
-----
    python scripts/fetch_playlist.py
    python scripts/fetch_playlist.py --playlist PLYDHfwsEk0RY
    python scripts/fetch_playlist.py --no-watch-pages
    python scripts/fetch_playlist.py --output data/playlist.json

Environment
-----------
    YOUTUBE_API_KEY   optional, enables the official API path
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAYLIST = "https://www.youtube.com/playlist?list=PLYDHfwsEk0RY"
DEFAULT_CHANNEL = "https://www.youtube.com/@EINITIAL24"
API_ROOT = "https://www.googleapis.com/youtube/v3"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)


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

# The chapter modules used by the course. Chapters are ordered chronologically,
# the playlist itself is ordered newest-first.
MODULES = [
    (1, 4, "Module 1: Getting Started with Kali Linux"),
    (5, 19, "Module 2: Linux Fundamentals for Ethical Hackers"),
    (20, 31, "Module 3: Networking, Anonymity & Traffic Routing"),
    (32, 41, "Module 4: Reconnaissance & Network Scanning"),
    (42, 48, "Module 5: Web Application & Vulnerability Analysis"),
    (49, 59, "Module 6: Password Attacks & Hash Cracking"),
    (60, 66, "Module 7: Sniffing, Spoofing & Traffic Analysis"),
    (67, 70, "Module 8: Wireless Network Security"),
    (71, 76, "Module 9: Exploitation, Honeypots & Advanced Topics"),
]


def module_for(chapter: int | None) -> str | None:
    if not chapter:
        return None
    for start, end, name in MODULES:
        if start <= chapter <= end:
            return name
    return None


def playlist_id_from(value: str) -> str:
    """Accept a playlist URL, a bare ID, or a URL with extra parameters."""
    value = value.strip()
    if "list=" in value:
        query = urllib.parse.urlparse(value).query
        params = urllib.parse.parse_qs(query)
        if params.get("list"):
            return params["list"][0]
    if re.fullmatch(r"[A-Za-z0-9_-]{10,50}", value):
        return value
    raise SystemExit(f"Could not read a playlist ID from: {value}")


def http_get(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def http_json(url: str, timeout: int = 30) -> dict:
    return json.loads(http_get(url, timeout=timeout))


def iso8601_duration_to_seconds(value: str | None) -> int | None:
    if not value:
        return None
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value)
    if not match:
        return None
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_display(seconds: int | None) -> str | None:
    if seconds is None:
        return None
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def date_only(value: str | None) -> str | None:
    if not value:
        return None
    return value[:10]


def parse_chapter(title: str) -> int | None:
    """Read an explicit chapter number from a title, e.g. 'Ch. 12' or 'Chapter 5'."""
    patterns = [
        r"\bChapter\s*(\d{1,3})\b",
        r"\bCh\.?\s*(\d{1,3})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, title, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def infer_chapters(videos: list[dict]) -> None:
    """Fill missing chapter numbers from neighbouring numbered videos.

    The playlist is chronological but ordered newest-first, so chapter numbers
    decrease with playlist position. Only positions between two known chapters
    with a consistent one-chapter-per-position step are inferred; everything
    else stays ``null`` with ``chapter_source`` set accordingly.
    """
    known = [(v["position"], v["chapter"]) for v in videos if v.get("chapter")]
    for video in videos:
        if video.get("chapter"):
            video["chapter_source"] = "title"
            continue
        video["chapter"] = None
        video["chapter_source"] = "unavailable"

    for video in videos:
        if video.get("chapter"):
            continue
        position = video["position"]
        before = [pair for pair in known if pair[0] < position]
        after = [pair for pair in known if pair[0] > position]
        if not before or not after:
            continue
        pos_before, chapter_before = max(before)
        pos_after, chapter_after = min(after)
        gap = pos_after - pos_before
        if gap <= 0:
            continue
        if abs(chapter_before - chapter_after) != gap:
            continue
        video["chapter"] = chapter_before - (position - pos_before)
        video["chapter_source"] = "inferred_from_neighbouring_chapters"


# ---------------------------------------------------------------------------
# YouTube Data API v3 path
# ---------------------------------------------------------------------------


def fetch_with_api(playlist_id: str, api_key: str) -> tuple[dict, list[dict], list[str]]:
    warnings: list[str] = []
    playlist_params = urllib.parse.urlencode(
        {"part": "snippet", "id": playlist_id, "key": api_key}
    )
    playlist = http_json(f"{API_ROOT}/playlists?{playlist_params}")
    if not playlist.get("items"):
        raise SystemExit(
            "The YouTube API returned no playlist for this ID. "
            "Check that the playlist is public and that the API key is valid."
        )
    playlist_info = playlist["items"][0]["snippet"]
    channel_id = playlist_info.get("channelId")
    channel_title = playlist_info.get("channelTitle")
    channel_url = f"https://www.youtube.com/channel/{channel_id}" if channel_id else None

    entries: list[dict] = []
    page_token = None
    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token
        page = http_json(f"{API_ROOT}/playlistItems?{urllib.parse.urlencode(params)}")
        for item in page.get("items", []):
            snippet = item.get("snippet", {})
            resource = snippet.get("resourceId", {})
            entries.append(
                {
                    "position": snippet.get("position", len(entries)) + 1,
                    "video_id": resource.get("videoId") or item.get("contentDetails", {}).get("videoId"),
                    "title": snippet.get("title") or "Unavailable video",
                    "description": snippet.get("description") or "",
                    "published_date": date_only(snippet.get("publishedAt")),
                    "thumbnail_url": (
                        snippet.get("thumbnails", {}).get("maxres")
                        or snippet.get("thumbnails", {}).get("high")
                        or {}
                    ).get("url"),
                    "playlist_item_published_at": snippet.get("publishedAt"),
                    "metadata_status": "api_playlist_item",
                }
            )
        page_token = page.get("nextPageToken")
        if not page_token:
            break
        time.sleep(0.2)

    # Enrich with video-level details (duration, real publish date, tags).
    ids = [entry["video_id"] for entry in entries if entry.get("video_id")]
    details: dict[str, dict] = {}
    for start in range(0, len(ids), 50):
        batch = ids[start : start + 50]
        params = urllib.parse.urlencode(
            {"part": "snippet,contentDetails,statistics,status", "id": ",".join(batch), "key": api_key}
        )
        data = http_json(f"{API_ROOT}/videos?{params}")
        for item in data.get("items", []):
            details[item["id"]] = item
        time.sleep(0.2)

    videos: list[dict] = []
    for entry in entries:
        item = details.get(entry["video_id"])
        entry["status"] = "published"
        entry["duration_seconds"] = None
        entry["upload_date"] = None
        entry["keywords"] = []
        entry["view_count"] = None
        entry["captions_available"] = None
        if item:
            snippet = item.get("snippet", {})
            entry["title"] = snippet.get("title") or entry["title"]
            entry["description"] = snippet.get("description") or entry["description"]
            entry["upload_date"] = date_only(snippet.get("publishedAt"))
            entry["published_date"] = entry["upload_date"] or entry["published_date"]
            entry["duration_seconds"] = iso8601_duration_to_seconds(
                item.get("contentDetails", {}).get("duration")
            )
            entry["keywords"] = snippet.get("tags") or []
            entry["view_count"] = (item.get("statistics") or {}).get("viewCount")
            privacy = (item.get("status") or {}).get("privacyStatus")
            if privacy and privacy != "public":
                entry["status"] = "scheduled"
                entry["metadata_status"] = f"api_{privacy}"
        else:
            entry["status"] = "unavailable"
            entry["metadata_status"] = "api_video_missing"
            warnings.append(f"Video {entry['video_id']} is no longer available.")
        videos.append(entry)

    meta = {
        "playlist_id": playlist_id,
        "title": playlist_info.get("title"),
        "description": playlist_info.get("description"),
        "channel_name": channel_title,
        "channel_url": channel_url,
        "source": "youtube_data_api_v3",
        "source_url": f"https://www.youtube.com/playlist?list={playlist_id}",
    }
    return meta, videos, warnings


# ---------------------------------------------------------------------------
# Public page fallback
# ---------------------------------------------------------------------------


def extract_initial_data(html: str) -> dict:
    match = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not match:
        raise SystemExit(
            "Could not read playlist data from the public page. "
            "YouTube may have changed its page format. Try again later or set YOUTUBE_API_KEY."
        )
    return json.loads(match.group(1))


def walk_for_lockups(node) -> list[dict]:
    found: list[dict] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "lockupViewModel" and value.get("contentId"):
                found.append(value)
            else:
                found.extend(walk_for_lockups(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(walk_for_lockups(value))
    return found


def fetch_playlist_page(playlist_id: str) -> tuple[dict, list[dict]]:
    url = f"https://www.youtube.com/playlist?list={playlist_id}&hl=en&gl=US"
    html = http_get(url)
    data = extract_initial_data(html)
    header = (
        data.get("header", {}).get("playlistHeaderRenderer")
        or data.get("metadata", {}).get("playlistMetadataRenderer")
        or {}
    )
    lockups = walk_for_lockups(data.get("contents", {}))

    title = None
    description = None
    if "title" in header:
        title = header["title"].get("simpleText") or "".join(
            run.get("text", "") for run in header["title"].get("runs", [])
        )
    description = (
        header.get("descriptionText", {}).get("simpleText")
        or header.get("description")
        or data.get("metadata", {}).get("playlistMetadataRenderer", {}).get("description")
    )

    # Fall back to the microformat if the header is a different shape.
    micro = data.get("microformat", {}).get("microformatDataRenderer", {})
    title = title or micro.get("title") or data.get("metadata", {}).get("playlistMetadataRenderer", {}).get("title")
    description = description or micro.get("description")

    entries = []
    for index, lockup in enumerate(lockups, start=1):
        meta = lockup.get("metadata", {}).get("lockupMetadataViewModel", {})
        video_id = lockup.get("contentId")
        duration = None
        try:
            overlays = lockup["contentImage"]["thumbnailViewModel"]["overlays"]
            for overlay in overlays:
                for badge in overlay.get("thumbnailBottomOverlayViewModel", {}).get("badges", []):
                    text = badge.get("thumbnailBadgeViewModel", {}).get("text")
                    if text:
                        duration = text
        except (KeyError, TypeError):
            pass
        entries.append(
            {
                "position": index,
                "video_id": video_id,
                "title": meta.get("title", {}).get("content") or "Unavailable video",
                "duration_display": None if duration == "Upcoming" else duration,
                "status": "scheduled" if duration == "Upcoming" else "published",
                "metadata_status": "public_playlist_page",
                "description": "",
                "published_date": None,
                "upload_date": None,
                "thumbnail_url": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
                "keywords": [],
                "view_count": None,
                "captions_available": None,
            }
        )
    meta = {
        "playlist_id": playlist_id,
        "title": title,
        "description": description,
        "channel_name": "EINITIAL24 ACADEMY",
        "channel_url": DEFAULT_CHANNEL,
        "source": "public_youtube_pages",
        "source_url": f"https://www.youtube.com/playlist?list={playlist_id}",
    }
    return meta, entries


def enrich_from_watch_page(video: dict, delay: float = 0.35) -> None:
    """Read description, exact duration, publish date and caption tracks."""
    video_id = video["video_id"]
    url = f"https://www.youtube.com/watch?v={video_id}&hl=en&gl=US"
    try:
        html = http_get(url)
    except Exception as error:  # noqa: BLE001 - network errors are reported, not raised
        video["metadata_status"] = f"watch_page_error: {error}"
        return

    match = re.search(r"var ytInitialPlayerResponse = (\{.*?\});(?:var|</script>)", html, re.S)
    if not match:
        video["metadata_status"] = "watch_page_without_player_response"
        return
    try:
        player = json.loads(match.group(1))
    except json.JSONDecodeError:
        video["metadata_status"] = "watch_page_json_error"
        return

    details = player.get("videoDetails", {}) or {}
    micro = player.get("microformat", {}).get("playerMicroformatRenderer", {}) or {}
    playability = player.get("playabilityStatus", {}) or {}
    captions = (
        player.get("captions", {})
        .get("playerCaptionsTracklistRenderer", {})
        .get("captionTracks", [])
    )

    if details.get("title"):
        video["title"] = details["title"]
    if details.get("shortDescription"):
        video["description"] = details["shortDescription"]
    if details.get("lengthSeconds"):
        video["duration_seconds"] = int(details["lengthSeconds"])
    if details.get("keywords"):
        video["keywords"] = details["keywords"]
    if details.get("viewCount") is not None:
        video["view_count"] = details["viewCount"]
    if micro.get("publishDate"):
        video["upload_date"] = date_only(micro["publishDate"])
        video["published_date"] = video["upload_date"]
        video["published_at"] = micro["publishDate"]
    video["captions_available"] = bool(captions)
    video["caption_languages"] = sorted({c.get("languageCode") for c in captions if c.get("languageCode")})
    video["playability_status"] = playability.get("status")
    if playability.get("status") == "OK":
        video["status"] = "published"
        video["metadata_status"] = "public_watch_page"
    elif playability.get("status") in {"LIVE_STREAM_OFFLINE", "UNPLAYABLE"}:
        # Scheduled premieres / not-yet-public videos return LIVE_STREAM_OFFLINE.
        video["status"] = "scheduled"
        video["metadata_status"] = f"public_watch_page:{playability.get('status')}"
        video["duration_seconds"] = None
        video["published_date"] = None
        video["captions_available"] = False
    else:
        video["status"] = "unavailable"
        video["metadata_status"] = f"public_watch_page:{playability.get('status')}"
    if delay:
        time.sleep(delay)


def fetch_with_public_pages(playlist_id: str, watch_pages: bool) -> tuple[dict, list[dict], list[str]]:
    warnings: list[str] = []
    meta, videos = fetch_playlist_page(playlist_id)
    if watch_pages:
        for video in videos:
            if video.get("video_id"):
                enrich_from_watch_page(video)
            if video["status"] == "published" and not video.get("description"):
                warnings.append(f"No description could be read for {video['video_id']}.")
    else:
        warnings.append("Watch pages were skipped; descriptions and dates are unavailable.")
    return meta, videos, warnings


# ---------------------------------------------------------------------------
# Normalisation and output
# ---------------------------------------------------------------------------


def normalise(meta: dict, videos: list[dict]) -> tuple[dict, dict]:
    for video in videos:
        video["chapter"] = parse_chapter(video.get("title") or "")
        video["url"] = f"https://www.youtube.com/watch?v={video['video_id']}"
        video["thumbnail_url"] = (
            f"https://i.ytimg.com/vi/{video['video_id']}/maxresdefault.jpg"
        )
        video["duration"] = seconds_to_display(video.get("duration_seconds"))
        if video.get("status") == "published" and not video.get("duration"):
            video["duration"] = video.get("duration_display")
        video["module"] = module_for(video.get("chapter"))
        video["has_description"] = bool((video.get("description") or "").strip())
        video["topics"] = sorted(
            {
                re.sub(r"^#", "", tag).strip()
                for tag in (video.get("keywords") or [])
                if isinstance(tag, str) and tag.strip()
            }
        )[:12]
        # Drop helper fields that are only useful during extraction.
        video.pop("duration_display", None)
        video.pop("playlist_item_published_at", None)
        video.pop("published_at", None)
        video.pop("caption_languages", None)

    infer_chapters(videos)
    for video in videos:
        video["module"] = module_for(video.get("chapter"))

    videos.sort(key=lambda item: item["position"])

    published = [v for v in videos if v.get("status") == "published"]
    scheduled = [v for v in videos if v.get("status") == "scheduled"]
    other = [v for v in videos if v.get("status") not in {"published", "scheduled"}]

    extraction_date = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    metadata = {
        "playlist_title": meta.get("title"),
        "playlist_id": meta.get("playlist_id"),
        "playlist_url": f"https://www.youtube.com/playlist?list={meta.get('playlist_id')}",
        "channel_name": meta.get("channel_name") or "EINITIAL24 ACADEMY",
        "channel_url": meta.get("channel_url") or DEFAULT_CHANNEL,
        "brand_website": "https://einitial24.com/",
        "extraction_date": extraction_date.split("T")[0],
        "extraction_timestamp_utc": extraction_date,
        "extraction_source": meta.get("source"),
        "total_videos": len(videos),
        "published_videos": len(published),
        "scheduled_videos": len(scheduled),
        "unavailable_videos": len(other),
        "chapters_min": min((v["chapter"] for v in videos if v.get("chapter")), default=None),
        "chapters_max": max((v["chapter"] for v in videos if v.get("chapter")), default=None),
        "description": meta.get("description"),
        "playlist_thumbnail": next(
            (v.get("thumbnail_url") for v in videos if v.get("video_id")), None
        ),
        "notes": [
            "Video titles, descriptions, durations and dates come from YouTube metadata.",
            "Scheduled chapters have no public description or duration yet; those values are null.",
            "Chapter numbers are read from titles where present and otherwise inferred from neighbours.",
            "Transcripts are not stored in this repository.",
        ],
    }
    payload = {
        "schema_version": 1,
        "generated_by": "scripts/fetch_playlist.py",
        "playlist": metadata,
        "videos": videos,
    }
    return payload, metadata


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--playlist", default=os.environ.get("PLAYLIST_URL", DEFAULT_PLAYLIST))
    parser.add_argument("--api-key", default=os.environ.get("YOUTUBE_API_KEY", ""))
    parser.add_argument("--output", default="data/playlist.json")
    parser.add_argument("--metadata-output", default="data/playlist-metadata.json")
    parser.add_argument("--no-watch-pages", action="store_true", help="skip per-video watch page requests")
    parser.add_argument("--force-public", action="store_true", help="ignore an available API key")
    args = parser.parse_args(argv)

    playlist_id = playlist_id_from(args.playlist)
    print(f"Playlist ID: {playlist_id}")

    warnings: list[str]
    if args.api_key and not args.force_public:
        print("Source: YouTube Data API v3")
        meta, videos, warnings = fetch_with_api(playlist_id, args.api_key)
    else:
        print("Source: public YouTube pages (set YOUTUBE_API_KEY for the official API)")
        meta, videos, warnings = fetch_with_public_pages(
            playlist_id, watch_pages=not args.no_watch_pages
        )

    payload, metadata = normalise(meta, videos)
    payload["warnings"] = warnings

    write_json(ROOT / args.output, payload)
    write_json(ROOT / args.metadata_output, metadata)

    print(
        f"Done: {metadata['total_videos']} videos "
        f"({metadata['published_videos']} published, {metadata['scheduled_videos']} scheduled)."
    )
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
