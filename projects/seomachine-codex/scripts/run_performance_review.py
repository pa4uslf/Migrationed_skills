#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from seo_machine_common import utc_timestamp, write_text


def load_aggregator():
    try:
        from data_sources.modules.data_aggregator import DataAggregator
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Python dependency while loading analytics modules. "
            "Install requirements with `.venv/bin/pip install -r data_sources/requirements.txt`."
        ) from exc
    return DataAggregator


def priority_emoji(priority: str) -> str:
    return {
        "high": "🔥",
        "medium": "⚠️",
        "low": "ℹ️",
    }.get(priority, "•")


def render_recommendations(recommendations: List[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    if not recommendations:
        return ["- No prioritized recommendations were returned."]

    for index, rec in enumerate(recommendations, 1):
        lines.append(f"{index}. {priority_emoji(rec.get('priority', 'low'))} {rec.get('action', 'Untitled action')}")
        lines.append(f"   - Priority: {rec.get('priority', 'unknown')}")
        lines.append(f"   - Type: {rec.get('type', 'unknown')}")
        lines.append(f"   - Reason: {rec.get('reason', 'No reason provided')}")
    return lines


def summarize_item(item: Dict[str, Any]) -> str:
    preferred_keys = [
        "keyword",
        "query",
        "title",
        "url",
        "path",
        "position",
        "impressions",
        "clicks",
        "ctr",
        "change_percent",
        "recent_impressions",
        "missed_clicks",
    ]

    parts = []
    for key in preferred_keys:
        value = item.get(key)
        if value in (None, "", [], {}):
            continue
        parts.append(f"{key}={value}")

    if not parts:
        parts = [f"{key}={value}" for key, value in item.items() if value not in (None, "", [], {})][:6]

    return ", ".join(parts) if parts else "No details returned"


def build_report(days: int) -> str:
    DataAggregator = load_aggregator()
    aggregator = DataAggregator()
    report = aggregator.generate_performance_report(days=days)
    opportunities = report.get("opportunities", {})
    summary = report.get("summary", {})

    lines = [
        "# Performance Review",
        "",
        f"- Generated: {utc_timestamp()}",
        f"- Analysis Period: Last {days} days",
        "",
        "## Summary",
        "",
        f"- Total Pageviews: {summary.get('total_pageviews', 'Unavailable')}",
        f"- Total Sessions: {summary.get('total_sessions', 'Unavailable')}",
        f"- Total Clicks: {summary.get('total_clicks', 'Unavailable')}",
        f"- Total Impressions: {summary.get('total_impressions', 'Unavailable')}",
        f"- Average CTR: {summary.get('avg_ctr', 'Unavailable')}",
        f"- Total Keywords: {summary.get('total_keywords', 'Unavailable')}",
        "",
        "## Opportunity Counts",
        "",
        f"- Quick Wins: {len(opportunities.get('quick_wins', []))}",
        f"- Declining Content: {len(opportunities.get('declining_content', []))}",
        f"- Low CTR Opportunities: {len(opportunities.get('low_ctr', []))}",
        f"- Trending Topics: {len(opportunities.get('trending_topics', []))}",
        f"- Competitor Gaps: {len(opportunities.get('competitor_gaps', []))}",
        "",
        "## Priority Queue",
        "",
    ]

    lines.extend(render_recommendations(report.get("recommendations", [])))
    lines.extend(["", "## Detailed Opportunities", ""])

    sections = [
        ("Quick Wins", opportunities.get("quick_wins", [])),
        ("Declining Content", opportunities.get("declining_content", [])),
        ("Low CTR Opportunities", opportunities.get("low_ctr", [])),
        ("Trending Topics", opportunities.get("trending_topics", [])),
        ("Competitor Gaps", opportunities.get("competitor_gaps", [])),
    ]

    for title, items in sections:
        lines.append(f"### {title}")
        lines.append("")
        if not items:
            lines.append("- No items returned.")
            lines.append("")
            continue

        for item in items[:10]:
            lines.append(f"- {summarize_item(item)}")
        lines.append("")

    lines.extend(
        [
            "## Next Actions",
            "",
            "1. Work the high-priority quick wins before creating brand-new content.",
            "2. Rewrite or refresh declining pages before the traffic loss compounds.",
            "3. Use `analyze-existing`, `rewrite`, `research`, and `write` skills to act on this queue.",
            "",
        ]
    )

    return "\n".join(lines)


def default_output(root: Path) -> Path:
    return root / "research" / f"performance-review-{utc_timestamp().split(' ')[0]}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Codex-friendly performance review report.")
    parser.add_argument("--days", type=int, default=30, help="Number of days to analyze")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    try:
        report = build_report(args.days)
    except RuntimeError as exc:
        parser.exit(1, f"{exc}\n")

    output = Path(args.output).resolve() if args.output else default_output(ROOT)
    write_text(output, report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
