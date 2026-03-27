#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent


def run_script(script_name: str, extra_args: List[str] | None = None) -> Tuple[str, int, str]:
    command = [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / script_name)]
    if extra_args:
        command.extend(extra_args)

    result = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return script_name, result.returncode, output.strip()


def scripts_for_mode(mode: str, include_gaps: bool) -> List[Tuple[str, List[str]]]:
    if mode == "quick":
        return [("research_quick_wins.py", [])]

    scripts: List[Tuple[str, List[str]]] = [
        ("research_quick_wins.py", []),
        ("research_performance_matrix.py", []),
        ("research_topic_clusters.py", []),
        ("research_trending.py", []),
    ]

    if include_gaps:
        scripts.insert(1, ("research_competitor_gaps.py", []))

    return scripts


def expected_reports(mode: str, include_gaps: bool) -> List[str]:
    today = datetime.now().strftime("%Y-%m-%d")
    reports = [f"research/quick-wins-{today}.md"]

    if mode == "quick":
        return reports

    if include_gaps:
        reports.append(f"research/competitor-gaps-{today}.md")

    reports.extend(
        [
            f"research/performance-matrix-{today}.md",
            f"research/topic-clusters-{today}.md",
            f"research/trending-{today}.md",
        ]
    )

    return reports


def render_summary(mode: str, include_gaps: bool, results: List[Tuple[str, int, str]]) -> str:
    has_failures = False
    lines = [
        "# Priorities Run Summary",
        "",
        f"- Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- Mode: {mode}",
        f"- Competitor Gaps Included: {'Yes' if include_gaps else 'No'}",
        "",
        "## Script Results",
        "",
    ]

    for script_name, code, output in results:
        output_lower = output.lower()
        has_error_markers = (
            "✗" in output
            or "error" in output_lower
            or "traceback" in output_lower
            or "not configured" in output_lower
            or "required for" in output_lower
        )
        if code != 0:
            status = f"FAIL ({code})"
            has_failures = True
        elif has_error_markers:
            status = "WARN"
            has_failures = True
        else:
            status = "PASS"
        lines.append(f"- `{script_name}` -> {status}")
        if output:
            preview = output.splitlines()[-5:]
            for line in preview:
                lines.append(f"  {line}")

    lines.extend(["", "## Expected Reports", ""])
    for report in expected_reports(mode, include_gaps):
        exists = (ROOT / report).exists()
        lines.append(f"- `{report}` -> {'present' if exists else 'missing'}")

    lines.extend(["", "## Recommended Next Steps", ""])
    if has_failures:
        lines.extend(
            [
                "1. Fix missing credentials or API configuration in `data_sources/config/.env` first.",
                "2. Re-run the priorities workflow after the data sources connect cleanly.",
                "3. Once reports are present, route existing URLs to `analyze-existing` / `rewrite` and new gaps to `research` / `article`.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "1. Open the newest quick-wins report first.",
                "2. Use `analyze-existing` or `rewrite` for existing pages that surfaced.",
                "3. Use `research` or `article` for new-content opportunities.",
                "",
            ]
        )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the SEO priorities workflow without interactive prompts.")
    parser.add_argument("--mode", choices=["quick", "comprehensive"], default="comprehensive")
    parser.add_argument("--skip-gaps", action="store_true", help="Skip competitor gap analysis in comprehensive mode")
    parser.add_argument("--output", help="Optional summary output path")
    args = parser.parse_args()

    include_gaps = args.mode == "comprehensive" and not args.skip_gaps
    results: List[Tuple[str, int, str]] = []

    for script_name, extra_args in scripts_for_mode(args.mode, include_gaps):
        results.append(run_script(script_name, extra_args))

    summary = render_summary(args.mode, include_gaps, results)
    output = Path(args.output).resolve() if args.output else ROOT / "research" / f"priorities-{datetime.now().strftime('%Y-%m-%d')}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(summary, encoding="utf-8")
    print(output)

    return 0 if all(code == 0 for _, code, _ in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
