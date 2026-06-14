#!/usr/bin/env python3
"""审计 CSV 中多轮标注列的一致性，并输出中文 Markdown 报告。"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


AUTO_HINTS = ("label", "tag", "class", "prediction", "标签", "分类", "预测")


def norm(value: str) -> str:
    return " ".join((value or "").strip().split())


def detect_label_columns(fieldnames: list[str], id_column: str) -> list[str]:
    return [
        name
        for name in fieldnames
        if name != id_column and any(hint in name.lower() for hint in AUTO_HINTS)
    ]


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description="审计重复标注的一致性。")
    parser.add_argument("input", help="CSV 文件：每行一个样本，包含多个标注列。")
    parser.add_argument("--id-column", default="id", help="样本 ID 列名。")
    parser.add_argument("--label-columns", help="逗号分隔的标签列；省略时自动检测。")
    parser.add_argument("--output", help="Markdown 报告路径；省略时打印到终端。")
    parser.add_argument("--top-n", type=int, default=50, help="最多展示多少条分歧样本。")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        if args.id_column not in fieldnames:
            raise SystemExit(f"缺少 ID 列：{args.id_column}")
        label_columns = (
            [col.strip() for col in args.label_columns.split(",") if col.strip()]
            if args.label_columns
            else detect_label_columns(fieldnames, args.id_column)
        )
        missing = [col for col in label_columns if col not in fieldnames]
        if missing:
            raise SystemExit(f"缺少标签列：{', '.join(missing)}")
        if len(label_columns) < 2:
            raise SystemExit("至少需要两个标签列。")
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
        "# 标注一致性审计",
        "",
        f"- 输入文件：`{input_path}`",
        f"- 样本数：{total}",
        f"- 标签列：{', '.join(f'`{c}`' for c in label_columns)}",
        f"- 完全一致：{exact} / {total}（{exact_rate:.1f}%）",
        f"- 存在分歧的行：{disagreement_count}",
        f"- 完全分歧的行：{len(complete_disagreements)}",
        f"- 建议人工审查行数：下方展示 {min(disagreement_count, args.top_n)} 行",
        "",
        "## 按标签统计的分歧集中度",
        "",
        "| 标签 | 出现次数 | 出现分歧的行数 |",
        "| --- | ---: | ---: |",
    ]
    for label, count in disagreement_by_label.most_common(20):
        lines.append(f"| {md_escape(label)} | {label_counts[label]} | {count} |")

    lines.extend(
        [
            "",
            "## 高频标签替代关系",
            "",
            "| 标签 A | 标签 B | 行数 |",
            "| --- | --- | ---: |",
        ]
    )
    for (left, right), count in pair_confusions.most_common(20):
        lines.append(f"| {md_escape(left)} | {md_escape(right)} | {count} |")

    lines.extend(
        [
            "",
            "## 人工审查队列",
            "",
            "| 优先级 | 样本 ID | 标签 | 原因 |",
            "| --- | --- | --- | --- |",
        ]
    )
    review_rows = complete_disagreements + partial_disagreements
    for item in review_rows[: args.top_n]:
        priority = "P1" if item in complete_disagreements else "P2"
        reason = "所有非空标签都不同" if item in complete_disagreements else "部分分歧或缺失标签"
        labels = "; ".join(f"{col}={label or '<空>'}" for col, label in zip(label_columns, item["labels"]))
        lines.append(f"| {priority} | {md_escape(item['id'])} | {md_escape(labels)} | {reason} |")

    lines.extend(
        [
            "",
            "## 建议下一步",
            "",
            "- 优先审查 P1 样本。",
            "- 如果某一组标签替代关系占比很高，先修订标签边界，再继续扩大标注。",
            "- 如果完全一致率低于验收阈值，先用示例做一轮校准。",
            "- 将最终报告记录到 `pm-memory/LABEL_AUDIT.md`。",
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
