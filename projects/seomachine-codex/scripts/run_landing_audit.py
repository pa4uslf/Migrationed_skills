#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from seo_machine_common import parse_article, read_text, utc_timestamp, write_text


def load_landing_dependencies():
    try:
        from data_sources.modules.above_fold_analyzer import analyze_above_fold
        from data_sources.modules.cta_analyzer import analyze_ctas
        from data_sources.modules.cro_checker import check_cro
        from data_sources.modules.landing_page_scorer import score_landing_page
        from data_sources.modules.trust_signal_analyzer import analyze_trust_signals
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Python dependency while loading landing-page analysis modules. "
            "Install requirements with `.venv/bin/pip install -r data_sources/requirements.txt`."
        ) from exc

    return {
        "analyze_above_fold": analyze_above_fold,
        "analyze_ctas": analyze_ctas,
        "check_cro": check_cro,
        "score_landing_page": score_landing_page,
        "analyze_trust_signals": analyze_trust_signals,
    }


def infer_landing_metadata(parsed: Dict[str, Any], page_type: str, goal: str) -> Tuple[str, str, str]:
    metadata = parsed["metadata"]
    body = parsed["body"]

    meta_title = metadata.get("meta title", parsed["title"])
    meta_description = metadata.get("meta description", "")
    target_keyword = metadata.get("target keyword") or metadata.get("primary keyword") or ""
    resolved_page_type = metadata.get("page type", page_type)
    resolved_goal = metadata.get("conversion goal", goal)

    if not meta_description:
        intro = " ".join(body.splitlines()[:3]).strip()
        intro = re.sub(r"\s+", " ", intro)
        meta_description = intro[:157] + "..." if len(intro) > 160 else intro

    return meta_title, meta_description, target_keyword, resolved_page_type, resolved_goal


def build_report(file_path: Path, page_type: str, goal: str) -> str:
    deps = load_landing_dependencies()
    parsed = parse_article(read_text(file_path))
    content = parsed["body"]
    meta_title, meta_description, target_keyword, page_type, goal = infer_landing_metadata(parsed, page_type, goal)

    landing_score = deps["score_landing_page"](
        content=content,
        page_type=page_type,
        conversion_goal=goal,
        meta_title=meta_title or None,
        meta_description=meta_description or None,
        primary_keyword=target_keyword or None,
    )
    above_fold = deps["analyze_above_fold"](content)
    cta = deps["analyze_ctas"](content, conversion_goal=goal)
    trust = deps["analyze_trust_signals"](content)
    cro = deps["check_cro"](content, page_type=page_type, conversion_goal=goal)

    lines = [
        "# Landing Page Audit Report",
        "",
        f"- Generated: {utc_timestamp()}",
        f"- File: `{file_path}`",
        f"- Page Type: {page_type}",
        f"- Conversion Goal: {goal}",
        f"- Target Keyword: {target_keyword or 'Not set'}",
        "",
        "## Executive Summary",
        "",
        f"- Landing Page Score: {landing_score.get('overall_score', 'N/A')}/100",
        f"- Grade: {landing_score.get('grade', 'N/A')}",
        f"- Publishing Ready: {'Yes' if landing_score.get('publishing_ready') else 'No'}",
        f"- Above-the-Fold Score: {above_fold.get('overall_score', 'N/A')}/100",
        f"- CTA Effectiveness: {cta.get('summary', {}).get('overall_effectiveness', 'N/A')}/100",
        f"- Trust Signal Score: {trust.get('overall_score', 'N/A')}/100",
        f"- CRO Checklist Score: {cro.get('score', 'N/A')}/100",
        "",
        "## Critical Issues",
        "",
    ]

    critical = landing_score.get("critical_issues", [])
    if not critical:
        lines.append("- None")
    else:
        for item in critical:
            lines.append(f"- {item}")

    lines.extend(["", "## Above-the-Fold Analysis", ""])
    lines.extend(
        [
            f"- Passes 5-Second Test: {'Yes' if above_fold.get('passes_5_second_test') else 'No'}",
            f"- Headline: {above_fold.get('headline', {}).get('text', 'N/A')}",
            f"- Headline Quality: {above_fold.get('headline', {}).get('quality', 'N/A')}",
            f"- First CTA: {above_fold.get('cta', {}).get('first_cta', 'Not found')}",
            f"- Trust Signal Present Above Fold: {'Yes' if above_fold.get('trust_signal', {}).get('present') else 'No'}",
            "",
        ]
    )

    if above_fold.get("recommendations"):
        lines.append("Recommendations:")
        for item in above_fold["recommendations"][:8]:
            lines.append(f"- {item}")
        lines.append("")

    lines.extend(["## CTA Analysis", ""])
    cta_summary = cta.get("summary", {})
    lines.extend(
        [
            f"- Total CTAs: {cta_summary.get('total_ctas', 'N/A')}",
            f"- Average CTA Quality: {cta_summary.get('average_quality_score', 'N/A')}/100",
            f"- Distribution Score: {cta_summary.get('distribution_score', 'N/A')}/100",
            f"- Goal Alignment Score: {cta_summary.get('goal_alignment_score', 'N/A')}/100",
            "",
        ]
    )
    if cta.get("recommendations"):
        lines.append("Recommendations:")
        for item in cta["recommendations"][:8]:
            lines.append(f"- [{item.get('priority', 'info')}] {item.get('recommendation', item.get('issue', 'No recommendation text'))}")
        lines.append("")

    lines.extend(["## Trust Signals", ""])
    lines.extend(
        [
            f"- Overall Trust Score: {trust.get('overall_score', 'N/A')}/100",
            f"- Testimonial Count: {trust.get('summary', {}).get('testimonial_count', 'N/A')}",
            f"- Customer Count Signals: {trust.get('summary', {}).get('customer_count_signals', 'N/A')}",
            f"- Risk Reversal Signals: {trust.get('summary', {}).get('risk_reversal_signals', 'N/A')}",
            "",
        ]
    )
    if trust.get("weaknesses"):
        lines.append("Weaknesses:")
        for item in trust["weaknesses"][:8]:
            lines.append(f"- {item}")
        lines.append("")

    lines.extend(["## CRO Checklist", ""])
    lines.extend(
        [
            f"- Score: {cro.get('score', 'N/A')}/100",
            f"- Passes Audit: {'Yes' if cro.get('passes_audit') else 'No'}",
            f"- Critical Failures: {cro.get('summary', {}).get('critical_failures', 'N/A')}",
            f"- Warnings: {cro.get('summary', {}).get('warnings', 'N/A')}",
            "",
        ]
    )
    if cro.get("critical_failures"):
        lines.append("Critical Failures:")
        for item in cro["critical_failures"]:
            lines.append(f"- {item}")
        lines.append("")

    lines.extend(["## Priority Action Items", ""])
    action_items = []
    action_items.extend(critical)
    action_items.extend(landing_score.get("warnings", []))
    action_items.extend([item.get("recommendation", item.get("issue", "")) for item in cta.get("recommendations", [])])
    action_items.extend(trust.get("weaknesses", []))
    deduped = []
    for item in action_items:
        if item and item not in deduped:
            deduped.append(item)

    if not deduped:
        lines.append("- No major action items returned.")
    else:
        for item in deduped[:12]:
            lines.append(f"- {item}")

    lines.append("")
    return "\n".join(lines)


def default_output(file_path: Path) -> Path:
    return file_path.with_name(f"landing-audit-{file_path.stem}.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a landing page file with the landing-page analysis modules.")
    parser.add_argument("file_path", help="Path to a local landing page Markdown file")
    parser.add_argument("--type", default="seo", choices=["seo", "ppc"], help="Landing page type")
    parser.add_argument("--goal", default="trial", choices=["trial", "demo", "lead"], help="Primary conversion goal")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    file_path = Path(args.file_path).resolve()

    try:
        report = build_report(file_path, page_type=args.type, goal=args.goal)
    except RuntimeError as exc:
        parser.exit(1, f"{exc}\n")

    output = Path(args.output).resolve() if args.output else default_output(file_path)
    write_text(output, report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
