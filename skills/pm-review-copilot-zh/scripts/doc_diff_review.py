#!/usr/bin/env python3
"""为两个文本草稿生成紧凑的中文 Markdown diff 报告。"""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path


def read_lines(path: str) -> list[str]:
    return Path(path).read_text(encoding="utf-8").splitlines()


def main() -> int:
    parser = argparse.ArgumentParser(description="比较两个 PRD/策略草稿。")
    parser.add_argument("previous", help="上一版草稿路径。")
    parser.add_argument("current", help="当前版草稿路径。")
    parser.add_argument("--output", help="Markdown 报告输出路径。不提供时打印到终端。")
    parser.add_argument("--context", type=int, default=2, help="diff 上下文行数。")
    args = parser.parse_args()

    previous = read_lines(args.previous)
    current = read_lines(args.current)
    diff = list(
        difflib.unified_diff(
            previous,
            current,
            fromfile=args.previous,
            tofile=args.current,
            lineterm="",
            n=args.context,
        )
    )

    added = [line[1:] for line in diff if line.startswith("+") and not line.startswith("+++")]
    removed = [line[1:] for line in diff if line.startswith("-") and not line.startswith("---")]

    lines = [
        "# 草稿 Diff 审查",
        "",
        f"- 上一版：`{args.previous}`",
        f"- 当前版：`{args.current}`",
        f"- 新增行数：{len(added)}",
        f"- 删除行数：{len(removed)}",
        "",
        "## 审查重点",
        "",
        "- 检查新增 claim 是否有证据支撑。",
        "- 检查被删除的约束、风险、开放问题和保留意见。",
        "- 检查指标定义、发布标准、标签规则是否发生变化。",
        "",
        "## 新增内容",
        "",
    ]
    lines.extend(f"- {line}" for line in added[:80] if line.strip())
    if len(added) > 80:
        lines.append(f"- ... 还有 {len(added) - 80} 行新增内容已省略")

    lines.extend(["", "## 删除内容", ""])
    lines.extend(f"- {line}" for line in removed[:80] if line.strip())
    if len(removed) > 80:
        lines.append(f"- ... 还有 {len(removed) - 80} 行删除内容已省略")

    lines.extend(["", "## 统一 Diff", "", "```diff"])
    lines.extend(diff[:300])
    if len(diff) > 300:
        lines.append(f"... 还有 {len(diff) - 300} 行 diff 已省略")
    lines.append("```")

    report = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
