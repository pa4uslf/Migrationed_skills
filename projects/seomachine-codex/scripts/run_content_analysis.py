#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from seo_machine_common import (
    article_slug,
    count_links,
    format_bullets,
    get_metadata_value,
    load_serp_results,
    parse_article,
    parse_keywords,
    read_text,
    report_path,
    utc_timestamp,
    word_count,
    write_text,
)


def load_analysis_dependencies() -> Dict[str, Any]:
    try:
        from data_sources.modules.content_length_comparator import compare_content_length
        from data_sources.modules.content_scorer import ContentScorer
        from data_sources.modules.keyword_analyzer import analyze_keywords
        from data_sources.modules.readability_scorer import ReadabilityScorer
        from data_sources.modules.search_intent_analyzer import analyze_intent
        from data_sources.modules.seo_quality_rater import rate_seo_quality
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Python dependency while loading SEO analysis modules. "
            "Install requirements with `pip install -r data_sources/requirements.txt`."
        ) from exc

    return {
        "compare_content_length": compare_content_length,
        "ContentScorer": ContentScorer,
        "analyze_keywords": analyze_keywords,
        "ReadabilityScorer": ReadabilityScorer,
        "analyze_intent": analyze_intent,
        "rate_seo_quality": rate_seo_quality,
    }


def build_report(
    article_path: Path,
    site_url: Optional[str] = None,
    serp_results: Optional[List[Dict[str, Any]]] = None,
) -> str:
    deps = load_analysis_dependencies()
    parsed = parse_article(read_text(article_path))
    metadata = parsed["metadata"]
    content = parsed["body"]
    title = parsed["title"]
    primary_keyword = get_metadata_value(metadata, "primary keyword")
    secondary_keywords = parse_keywords(get_metadata_value(metadata, "secondary keywords"))
    meta_title = get_metadata_value(metadata, "meta title") or ""
    meta_description = get_metadata_value(metadata, "meta description") or ""
    counts = count_links(content, site_url)
    total_words = word_count(content)

    scorer = deps["ContentScorer"]()
    quality = scorer.score(
        content,
        {
            "meta_title": meta_title,
            "meta_description": meta_description,
            "primary_keyword": primary_keyword or "",
            "secondary_keywords": secondary_keywords,
        },
    )

    intent = deps["analyze_intent"](primary_keyword) if primary_keyword else None
    keyword_result = (
        deps["analyze_keywords"](content, primary_keyword, secondary_keywords or None)
        if primary_keyword
        else None
    )
    readability = deps["ReadabilityScorer"]().analyze(content)
    seo_result = deps["rate_seo_quality"](
        content=content,
        meta_title=meta_title or None,
        meta_description=meta_description or None,
        primary_keyword=primary_keyword,
        secondary_keywords=secondary_keywords or None,
        keyword_density=(
            keyword_result["primary_keyword"]["density"] if keyword_result else None
        ),
        internal_link_count=counts["internal"],
        external_link_count=counts["external"],
    )

    length_result = None
    if primary_keyword and serp_results:
        length_result = deps["compare_content_length"](
            keyword=primary_keyword,
            your_word_count=total_words,
            serp_results=serp_results,
            fetch_content=True,
        )

    action_items = []
    for fix in quality.get("priority_fixes", []):
        action_items.append(f"[{fix['dimension']}] {fix['issue']} -> {fix['fix']}")

    if seo_result.get("critical_issues"):
        for issue in seo_result["critical_issues"]:
            action_items.append(f"[seo] {issue}")

    if not action_items:
        action_items.append("No critical blockers detected. Review the detailed sections for smaller improvements.")

    lines = [
        f"# Content Analysis Report: {title}",
        "",
        f"- Generated: {utc_timestamp()}",
        f"- Article: `{article_path}`",
        f"- Word Count: {total_words}",
        f"- Primary Keyword: {primary_keyword or 'Not set'}",
        f"- Secondary Keywords: {', '.join(secondary_keywords) if secondary_keywords else 'None'}",
        "",
        "## Executive Summary",
        "",
        f"- Composite Quality Score: {quality['composite_score']}/100",
        f"- Passed Quality Threshold: {'Yes' if quality['passed'] else 'No'}",
        f"- SEO Score: {seo_result.get('overall_score', 'N/A')}/100",
        f"- Internal Links: {counts['internal']}",
        f"- External Links: {counts['external']}",
        "",
        "## Search Intent",
        "",
    ]

    if intent:
        lines.extend(
            [
                f"- Primary Intent: {intent.get('primary_intent', 'unknown')}",
                f"- Secondary Intent: {intent.get('secondary_intent', 'none')}",
                f"- Confidence: {intent.get('confidence', 'N/A')}",
                "",
                "Recommendations:",
                format_bullets(intent.get("recommendations", [])[:6]) or "- No recommendations returned.",
                "",
            ]
        )
    else:
        lines.extend(["- Primary keyword missing, so intent analysis was skipped.", ""])

    lines.extend(["## Keyword Optimization", ""])
    if keyword_result:
        primary = keyword_result["primary_keyword"]
        placements = primary.get("critical_placements", {})
        lines.extend(
            [
                f"- Density: {primary.get('density', 'N/A')}%",
                f"- Status: {primary.get('density_status', 'unknown')}",
                f"- Total Occurrences: {primary.get('total_occurrences', 'N/A')}",
                f"- In H1: {'Yes' if placements.get('in_h1') else 'No'}",
                f"- In First 100 Words: {'Yes' if placements.get('in_first_100_words') else 'No'}",
                f"- In H2 Headings: {placements.get('in_h2_count', 0)}",
                f"- Stuffing Risk: {keyword_result.get('keyword_stuffing', {}).get('risk_level', 'unknown')}",
                "",
                "Recommendations:",
                format_bullets(keyword_result.get("recommendations", [])[:8]) or "- No keyword recommendations returned.",
                "",
            ]
        )
    else:
        lines.extend(["- Primary keyword missing, so keyword analysis was skipped.", ""])

    lines.extend(["## Readability", ""])
    readability_metrics = readability.get("readability_metrics", {})
    readability_structure = readability.get("structure_analysis", {})
    readability_complexity = readability.get("complexity_analysis", {})
    lines.extend(
        [
            f"- Overall Readability Score: {readability.get('overall_score', 'N/A')}",
            f"- Grade: {readability.get('grade', 'N/A')}",
            f"- Flesch Reading Ease: {readability_metrics.get('flesch_reading_ease', 'N/A')}",
            f"- Flesch-Kincaid Grade: {readability_metrics.get('flesch_kincaid_grade', 'N/A')}",
            f"- Average Sentence Length: {readability_structure.get('avg_sentence_length', 'N/A')}",
            f"- Average Sentences Per Paragraph: {readability_structure.get('avg_sentences_per_paragraph', 'N/A')}",
            f"- Passive Sentence Ratio: {readability_complexity.get('passive_sentence_ratio', 'N/A')}%",
            "",
        ]
    )
    recommendations = readability.get("recommendations", [])
    lines.extend(
        [
            "Recommendations:",
            format_bullets(recommendations[:8]) or "- No readability recommendations returned.",
            "",
        ]
    )

    lines.extend(["## SEO Quality", ""])
    lines.extend(
        [
            f"- Overall Score: {seo_result.get('overall_score', 'N/A')}/100",
            f"- Grade: {seo_result.get('grade', 'N/A')}",
            f"- Publishing Ready: {'Yes' if seo_result.get('publishing_ready') else 'No'}",
            "",
        ]
    )

    critical_issues = seo_result.get("critical_issues", [])
    warnings = seo_result.get("warnings", [])
    suggestions = seo_result.get("suggestions", [])

    lines.extend(
        [
            "Critical Issues:",
            format_bullets(critical_issues) or "- None",
            "",
            "Warnings:",
            format_bullets(warnings) or "- None",
            "",
            "Suggestions:",
            format_bullets(suggestions[:8]) or "- None",
            "",
        ]
    )

    lines.extend(["## Content Length", ""])
    if length_result:
        if "error" in length_result:
            lines.extend([f"- {length_result['error']}", f"- {length_result.get('recommendation', 'No recommendation')}", ""])
        else:
            recommendation = length_result.get("recommendation", {})
            statistics = length_result.get("statistics", {})
            lines.extend(
                [
                    f"- Median Competitor Length: {statistics.get('median', 'N/A')}",
                    f"- 75th Percentile: {statistics.get('percentile_75', 'N/A')}",
                    f"- Recommended Minimum: {recommendation.get('recommended_min', 'N/A')}",
                    f"- Recommended Optimal: {recommendation.get('recommended_optimal', 'N/A')}",
                    f"- Your Status: {recommendation.get('your_status', 'N/A')}",
                    f"- Recommendation: {recommendation.get('message', 'N/A')}",
                    "",
                ]
            )
    else:
        lines.extend(["- No SERP JSON was supplied, so competitor length analysis was skipped.", ""])

    lines.extend(["## Priority Action Plan", "", format_bullets(action_items[:10]), ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Codex-friendly content analysis report.")
    parser.add_argument("article_path", help="Path to the article Markdown file")
    parser.add_argument("--site-url", help="Canonical site URL for internal vs external link counting")
    parser.add_argument("--serp-json", help="Optional JSON file containing SERP results")
    parser.add_argument("--output", help="Optional output path for the report")
    args = parser.parse_args()

    article_path = Path(args.article_path).resolve()
    serp_results = load_serp_results(Path(args.serp_json).resolve()) if args.serp_json else None
    try:
        report = build_report(article_path, site_url=args.site_url, serp_results=serp_results)
    except RuntimeError as exc:
        parser.exit(1, f"{exc}\n")
    output = Path(args.output).resolve() if args.output else report_path(article_path, "content-analysis")
    write_text(output, report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
