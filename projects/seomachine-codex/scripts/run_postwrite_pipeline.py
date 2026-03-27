#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_content_analysis import build_report
from seo_machine_common import (
    load_serp_results,
    parse_article,
    read_text,
    report_path,
    utc_timestamp,
    write_text,
)


def load_postwrite_dependencies():
    try:
        from data_sources.modules.content_scorer import ContentScorer
        from data_sources.modules.content_scrubber import scrub_file
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Python dependency while loading post-write modules. "
            "Install requirements with `pip install -r data_sources/requirements.txt`."
        ) from exc

    return ContentScorer, scrub_file


def quality_report_markdown(article_path: Path, result: dict) -> str:
    parsed = parse_article(read_text(article_path))
    lines = [
        f"# Quality Score Report: {parsed['title']}",
        "",
        f"- Generated: {utc_timestamp()}",
        f"- Article: `{article_path}`",
        f"- Composite Score: {result['composite_score']}/100",
        f"- Threshold: {result['threshold']}",
        f"- Passed: {'Yes' if result['passed'] else 'No'}",
        "",
        "## Dimension Breakdown",
        "",
        "| Dimension | Score | Weight |",
        "| --- | ---: | ---: |",
    ]

    for name, data in result["dimensions"].items():
        lines.append(f"| {name} | {data['score']} | {int(data['weight'] * 100)}% |")

    lines.extend(["", "## Priority Fixes", ""])

    fixes = result.get("priority_fixes", [])
    if not fixes:
        lines.append("- No priority fixes were returned.")
    else:
        for fix in fixes:
            lines.append(
                f"- [{fix['dimension']}] {fix['issue']} -> {fix['fix']}"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrub, score, and analyze a draft after writing.")
    parser.add_argument("article_path", help="Path to the draft Markdown file")
    parser.add_argument("--site-url", help="Canonical site URL for internal link counting")
    parser.add_argument("--serp-json", help="Optional JSON file with SERP results")
    args = parser.parse_args()

    article_path = Path(args.article_path).resolve()
    serp_results = load_serp_results(Path(args.serp_json).resolve()) if args.serp_json else None
    try:
        ContentScorer, scrub_file = load_postwrite_dependencies()
    except RuntimeError as exc:
        parser.exit(1, f"{exc}\n")

    scrub_file(str(article_path), verbose=True)

    parsed = parse_article(read_text(article_path))
    scorer = ContentScorer()
    quality = scorer.score(
        parsed["body"],
        {
            "meta_title": parsed["metadata"].get("meta title", ""),
            "meta_description": parsed["metadata"].get("meta description", ""),
            "primary_keyword": parsed["metadata"].get("primary keyword", ""),
            "secondary_keywords": parsed["metadata"].get("secondary keywords"),
        },
    )

    quality_path = report_path(article_path, "quality-report")
    write_text(quality_path, quality_report_markdown(article_path, quality))

    analysis_path = report_path(article_path, "content-analysis")
    try:
        analysis_report = build_report(article_path, site_url=args.site_url, serp_results=serp_results)
    except RuntimeError as exc:
        parser.exit(1, f"{exc}\n")
    write_text(analysis_path, analysis_report)

    print(f"quality_report={quality_path}")
    print(f"content_analysis={analysis_path}")

    if not quality["passed"]:
        print("Draft is below the quality threshold. Improve the article and re-run the pipeline.")
        return 2

    print("Draft passed the quality threshold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
