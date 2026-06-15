#!/usr/bin/env python3
"""Audit consistency across repeated labeling columns in a CSV."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


AUTO_HINTS = ("label", "tag", "class", "prediction")


def norm(value: str) -> str:
    return " ".join((value or "").strip().split())


def detect_label_columns(fieldnames: list[str], id_column: str) -> list[str]:
    candidates = [
        name
        for name in fieldnames
        if name != id_column and any(hint in name.lower() for hint in AUTO_HINTS)
    ]
    return candidates


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repeated labeling consistency.")
    parser.add_argument("input", help="CSV with one row per sample and repeated label columns.")
    parser.add_argument("--id-column", default="id")
    parser.add_argument("--label-columns", help="Comma-separated label columns. Auto-detected if omitted.")
    parser.add_argument("--output", help="Markdown report path. Prints to stdout if omitted.")
    parser.add_argument("--top-n", type=int, default=50, help="Max disagreement rows to show.")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        if args.id_column not in fieldnames:
            raise SystemExit(f"Missing id column: {args.id_column}")
        label_columns = (
            [col.strip() for col in args.label_columns.split(",") if col.strip()]
            if args.label_columns
            else detect_label_columns(fieldnames, args.id_column)
        )
        missing = [col for col in label_columns if col not in fieldnames]
        if missing:
            raise SystemExit(f"Missing label columns: {', '.join(missing)}")
        if len(label_columns) < 2:
            raise SystemExit("Need at least two label columns.")
        rows = list(reader)

    total = len(rows)
    exact = 0
    partial_disagreements = []
    complete_disagreements = []
    label_counts: Counter[str] = Counter()
    disagreement_by_label: Counter[str] = Counter()
    pair_confusions: Counter[tuple[str, str]] = Counter()

    for row in rows:
        labels = [norm(row.get(col, "")) for col in label_columns]
        non_empty = [label for label in labels if label]
        unique = sorted(set(non_empty))
        for label in non_empty:
            label_counts[label] += 1
        if len(unique) <= 1 and len(non_empty) == len(label_columns):
            exact += 1
            continue
        item = {
            "id": row.get(args.id_column, ""),
            "labels": labels,
            "unique": unique,
            "empty_count": len(label_columns) - len(non_empty),
        }
        if len(unique) == len(non_empty) and len(unique) > 1:
            complete_disagreements.append(item)
        else:
            partial_disagreements.append(item)
        for label in unique:
            disagreement_by_label[label] += 1
        for i, left in enumerate(unique):
            for right in unique[i + 1 :]:
                pair_confusions[(left, right)] += 1

    disagreement_count = total - exact
    exact_rate = (exact / total * 100) if total else 0.0

    lines = [
        "# Label Consistency Audit",
        "",
        f"- Input: `{input_path}`",
        f"- Samples: {total}",
        f"- Label columns: {', '.join(f'`{c}`' for c in label_columns)}",
        f"- Exact agreement: {exact} / {total} ({exact_rate:.1f}%)",
        f"- Disagreement rows: {disagreement_count}",
        f"- Complete disagreement rows: {len(complete_disagreements)}",
        f"- Suggested human review rows: {min(disagreement_count, args.top_n)} shown below",
        "",
        "## Disagreement Concentration By Label",
        "",
        "| Label | Total appearances | Disagreement rows |",
        "| --- | ---: | ---: |",
    ]
    for label, count in disagreement_by_label.most_common(20):
        lines.append(f"| {md_escape(label)} | {label_counts[label]} | {count} |")

    lines.extend(
        [
            "",
            "## Frequent Label Substitutions",
            "",
            "| Label A | Label B | Rows |",
            "| --- | --- | ---: |",
        ]
    )
    for (left, right), count in pair_confusions.most_common(20):
        lines.append(f"| {md_escape(left)} | {md_escape(right)} | {count} |")

    lines.extend(
        [
            "",
            "## Human Review Queue",
            "",
            "| Priority | Sample ID | Labels | Reason |",
            "| --- | --- | --- | --- |",
        ]
    )
    review_rows = complete_disagreements + partial_disagreements
    for item in review_rows[: args.top_n]:
        priority = "P1" if item in complete_disagreements else "P2"
        reason = "all non-empty labels differ" if item in complete_disagreements else "partial disagreement or missing label"
        labels = "; ".join(f"{col}={label or '<empty>'}" for col, label in zip(label_columns, item["labels"]))
        lines.append(f"| {priority} | {md_escape(item['id'])} | {md_escape(labels)} | {reason} |")

    lines.extend(
        [
            "",
            "## Suggested Next Actions",
            "",
            "- Review P1 rows first.",
            "- If one label pair dominates substitutions, revise taxonomy boundaries before scaling more labeling.",
            "- If exact agreement is below the acceptance threshold, run another calibration pass with examples.",
            "- Record the final report in `project-memory/LABEL_AUDIT.md`.",
        ]
    )

    report = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
