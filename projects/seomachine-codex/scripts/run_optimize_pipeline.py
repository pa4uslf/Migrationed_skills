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
from seo_machine_common import load_serp_results, report_path, write_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a final optimization audit for a draft.")
    parser.add_argument("article_path", help="Path to the article Markdown file")
    parser.add_argument("--site-url", help="Canonical site URL for internal link counting")
    parser.add_argument("--serp-json", help="Optional JSON file with SERP results")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    article_path = Path(args.article_path).resolve()
    serp_results = load_serp_results(Path(args.serp_json).resolve()) if args.serp_json else None
    report = build_report(article_path, site_url=args.site_url, serp_results=serp_results)
    output = Path(args.output).resolve() if args.output else report_path(article_path, "optimization-report")
    write_text(output, report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
