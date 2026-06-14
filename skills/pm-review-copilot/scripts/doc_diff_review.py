#!/usr/bin/env python3
"""Create a compact Markdown diff report for two text drafts."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path


def read_lines(path: str) -> list[str]:
    return Path(path).read_text(encoding="utf-8").splitlines()


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two PRD/strategy drafts.")
    parser.add_argument("previous")
    parser.add_argument("current")
    parser.add_argument("--output")
    parser.add_argument("--context", type=int, default=2)
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
        "# Draft Diff Review",
        "",
        f"- Previous: `{args.previous}`",
        f"- Current: `{args.current}`",
        f"- Added lines: {len(added)}",
        f"- Removed lines: {len(removed)}",
        "",
        "## Review Priorities",
        "",
        "- Check added claims for evidence.",
        "- Check removed constraints, risks, open questions, and caveats.",
        "- Check changed metric definitions, launch criteria, and label rules.",
        "",
        "## Added Lines",
        "",
    ]
    lines.extend(f"- {line}" for line in added[:80] if line.strip())
    if len(added) > 80:
        lines.append(f"- ... {len(added) - 80} more added lines omitted")

    lines.extend(["", "## Removed Lines", ""])
    lines.extend(f"- {line}" for line in removed[:80] if line.strip())
    if len(removed) > 80:
        lines.append(f"- ... {len(removed) - 80} more removed lines omitted")

    lines.extend(["", "## Unified Diff", "", "```diff"])
    lines.extend(diff[:300])
    if len(diff) > 300:
        lines.append(f"... {len(diff) - 300} more diff lines omitted")
    lines.append("```")

    report = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
