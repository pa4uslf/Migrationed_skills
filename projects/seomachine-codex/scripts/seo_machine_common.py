from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def parse_article(text: str) -> Dict[str, Any]:
    metadata, body = parse_frontmatter(text)
    inline_metadata, body = parse_inline_metadata(body)
    merged_metadata = {**inline_metadata, **metadata}
    h1 = extract_h1(body)
    if h1 and "meta title" not in merged_metadata:
        merged_metadata.setdefault("meta title", h1)
    return {
        "metadata": merged_metadata,
        "body": body.strip(),
        "title": h1 or merged_metadata.get("meta title") or "Untitled Article",
    }


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    marker = "\n---"
    end = text.find(marker, 4)
    if end == -1:
        return {}, text

    raw = text[4:end].strip()
    body = text[end + len(marker):].lstrip("\n")
    metadata: Dict[str, str] = {}

    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    return metadata, body


def parse_inline_metadata(text: str) -> Tuple[Dict[str, str], str]:
    lines = text.splitlines()
    metadata: Dict[str, str] = {}
    kept: List[str] = []
    metadata_done = False

    for index, line in enumerate(lines):
        stripped = line.strip()

        if stripped == "---":
            metadata_done = True
            continue

        if not metadata_done:
            match = re.match(r"^\*\*([^*]+)\*\*:\s*(.+?)\s*$", stripped)
            if match:
                key = match.group(1).strip().lower()
                value = match.group(2).strip()
                metadata[key] = value
                continue

        kept.append(line)

        if stripped and not stripped.startswith("#") and not re.match(r"^\*\*([^*]+)\*\*:\s*(.+?)\s*$", stripped):
            metadata_done = True

    body = "\n".join(kept).strip("\n")
    return metadata, body


def extract_h1(text: str) -> Optional[str]:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def get_metadata_value(metadata: Dict[str, str], key: str) -> Optional[str]:
    return metadata.get(key.lower())


def parse_keywords(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def article_slug(article_path: Path) -> str:
    stem = article_path.stem
    stem = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", stem)
    return stem


def report_path(article_path: Path, prefix: str) -> Path:
    slug = article_slug(article_path)
    return article_path.with_name(f"{prefix}-{slug}.md")


def markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)


def count_links(text: str, site_url: Optional[str] = None) -> Dict[str, int]:
    links = markdown_links(text)
    internal = 0
    external = 0

    site_host = urlparse(site_url).netloc if site_url else ""

    for _, url in links:
        parsed = urlparse(url)
        if not parsed.scheme and not parsed.netloc:
            internal += 1
            continue

        if site_host and parsed.netloc == site_host:
            internal += 1
        else:
            external += 1

    return {
        "internal": internal,
        "external": external,
        "total": len(links),
    }


def load_serp_results(path: Optional[Path]) -> Optional[List[Dict[str, Any]]]:
    if not path:
        return None

    payload = json.loads(read_text(path))

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ("results", "serp_results", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

    raise ValueError(f"Unsupported SERP payload format: {path}")


def format_bullets(items: Iterable[str]) -> str:
    lines = []
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines)
