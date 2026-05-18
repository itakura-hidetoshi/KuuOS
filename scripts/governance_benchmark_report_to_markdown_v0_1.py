#!/usr/bin/env python3

"""
KuuOS Governance Benchmark Markdown Report Generator v0.1

Converts the JSON governance benchmark report into a Markdown summary.

Boundary:
This report summarizes governance-oriented benchmark behavior only.
It does not grant theorem, institutional, deployment, clinical, or execution authority.
"""

from __future__ import annotations

import json
from pathlib import Path


REPORT_JSON = Path("benchmark_reports/governance_benchmark_report_v0_1.json")
REPORT_MD = Path("benchmark_reports/governance_benchmark_report_v0_1.md")


def main() -> None:
    report = json.loads(REPORT_JSON.read_text(encoding="utf-8"))

    lines: list[str] = []
    lines.append("# Governance Benchmark Report v0.1")
    lines.append("")
    lines.append(f"**Corpus:** {report['corpus']}")
    lines.append("")
    lines.append(f"**Total score:** {report['total_score']} / {report['max_total_score']}")
    lines.append("")
    lines.append(f"**Normalized score:** {report['normalized_score']:.3f}")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Case | Name | Score | Interpretation | Risk Tags |")
    lines.append("|---|---|---:|---|---|")

    for item in report["results"]:
        risk_tags = ", ".join(item.get("risk_tags", []))
        lines.append(
            f"| {item['case_id']} | {item['name']} | {item['score']} / {item['max_score']} | "
            f"{item['interpretation']} | {risk_tags} |"
        )

    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(report["non_authority_statement"])
    lines.append("")

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT_MD)


if __name__ == "__main__":
    main()
