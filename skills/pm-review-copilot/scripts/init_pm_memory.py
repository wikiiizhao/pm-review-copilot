#!/usr/bin/env python3
"""Create a PM review memory workspace."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


TEMPLATES: dict[str, str] = {
    "CONTEXT_MANIFEST.md": """# Context Manifest

## Project
- Name: {project_name}
- Owner:
- Memory root: `{memory_root}/`
- Documentation language:

## Read Order
1. `RECOVERY_NOTES.md`
2. `HUMAN_BRIEF.md`
3. `USER_PREFERENCES.md`
4. `CURRENT_STATE.md`
5. `DECISION_LOG.md`
6. `EVIDENCE_LOG.md`
7. `HYPOTHESIS_LAB.md`
8. `REVIEW_LOG.md`
9. `LABEL_AUDIT.md`
10. `MEMORY_UPDATE_LOG.md`

## Canonical Responsibilities
- User style and review preferences: `USER_PREFERENCES.md`
- Current truth: `CURRENT_STATE.md`
- Decisions and rationale: `DECISION_LOG.md`
- Evidence and source checks: `EVIDENCE_LOG.md`
- Unverified ideas: `HYPOTHESIS_LAB.md`
- Human review surface: `HUMAN_BRIEF.md`
- PRD/strategy review history: `REVIEW_LOG.md`
- Labeling audit history: `LABEL_AUDIT.md`
- Manual memory refresh history: `MEMORY_UPDATE_LOG.md`
- Resume handoff: `RECOVERY_NOTES.md`

## Conflict Policy
Use this priority for current-truth conflicts:
1. `CURRENT_STATE.md`
2. latest relevant `DECISION_LOG.md`
3. latest relevant `EVIDENCE_LOG.md`
4. latest `RECOVERY_NOTES.md`
5. `HUMAN_BRIEF.md`
6. `HYPOTHESIS_LAB.md`

Report conflicts before merging them.

## Ignore
- `.git/`
- `node_modules/`
- `dist/`
- `build/`
- `.cache/`
- `tmp/`
- generated exports unless explicitly requested
""",
    "USER_PREFERENCES.md": """# User Preferences

Use this file for the PM's working preferences. Do not treat preferences as project facts.

## Quick Setup Questions
Answer only what matters now.

1. Preferred language and tone:
2. Review style: strict | balanced | speed-first
3. Output length: concise | standard | detailed
4. What should always be called out?
5. What can usually be skipped?
6. Decision style: options first | recommendation first | risks first
7. Formatting preferences:
8. Recurring project context to remember:

## Current Preferences
- Language:
- Tone:
- Review strictness:
- Preferred summary shape:
- Tables: yes | no | only for audits
- Visual verdict: yes | no
- Human review tolerance:
- Always call out:
- Usually skip:
- Decision support style:

## Notes From Use
| Date | Preference learned | Source |
| --- | --- | --- |
""",
    "CURRENT_STATE.md": """# Current State

## Stable Facts
- 

## Metrics And Definitions
| Metric | Definition | Source | Last confirmed | Notes |
| --- | --- | --- | --- | --- |

## Active Operating Decisions
- 

## Current Context
- Current goal:
- Current phase:
- Main blocker:
- Next human decision:

## Constraints
- 

## Deprecated Or Retired
| Item | Replaced by | Reason | Date |
| --- | --- | --- | --- |
""",
    "DECISION_LOG.md": """# Decision Log

## YYYY-MM-DD - Decision title
- Status: adopted | rejected | deferred | superseded
- Context:
- Options considered:
- Decision:
- Rationale:
- Risks:
- Revisit when:
- Links to evidence:
""",
    "EVIDENCE_LOG.md": """# Evidence Log

## YYYY-MM-DD - Evidence title
- Source:
- Method:
- Finding:
- Confidence: low | medium | high
- Limitations:
- Affects:
- Related hypotheses:
""",
    "HYPOTHESIS_LAB.md": """# Hypothesis Lab

## Raw Sparks
- [ ] Hypothesis:
  - Why it might matter:
  - How to test:

## Working Hypotheses
### HYP-001 - Title
- Status: open | testing | promoted | dropped
- Claim:
- Evidence needed:
- Objections:
- Revisit when:
""",
    "HUMAN_BRIEF.md": """# Human Brief

## Attention Summary
- Current goal:
- Biggest risk:
- Next decision needed:
- Review load: low | medium | high

## Tracked Threads
| Thread | Status | Next action or blocker | Source |
| --- | --- | --- | --- |

## Must Check
- 

## Recently Changed
- 
""",
    "REVIEW_LOG.md": """# Review Log

## YYYY-MM-DD - Artifact title
- Artifact:
- Verdict: 🟢 pass | 🟡 needs local confirmation | 🔴 do not ship
- Human review load: 🟢 low | 🟡 medium | 🔴 high
- One-line summary:

### Must Check
| Priority | Location | Issue | Why it matters | Suggested action |
| --- | --- | --- | --- | --- |

### Claim Audit
| Type | Location | Claim | Evidence status | Risk | Action |
| --- | --- | --- | --- | --- | --- |

### Memory Conflicts
| Location | Draft says | Memory says | Source file | Resolution |
| --- | --- | --- | --- | --- |

### Drift From Previous Version
| Change type | Previous | Current | Risk |
| --- | --- | --- | --- |
""",
    "LABEL_AUDIT.md": """# Label Audit

## YYYY-MM-DD - Dataset or taxonomy
- Dataset:
- Label definition version:
- Runs compared:
- Exact agreement:
- Human review count:

### High-Risk Disagreements
| Sample ID | Labels | Risk reason | Suggested reviewer action |
| --- | --- | --- | --- |

### Taxonomy Issues
| Label pair | Symptom | Suggested definition change |
| --- | --- | --- |
""",
    "MEMORY_UPDATE_LOG.md": """# Memory Update Log

Use this log only for manual, user-triggered memory refreshes.

## YYYY-MM-DD HH:MM - Manual update
- Trigger/source:
- Files read:
- Files changed:
- Facts promoted:
- Hypotheses kept open:
- Conflicts or stale items found:
- Skipped as not durable:
- Next recommended refresh point:
""",
    "RECOVERY_NOTES.md": """# Recovery Notes

## {timestamp}
- What changed: PM memory workspace initialized.
- What is true now:
- What is blocked:
- Next action:
- Files to read first: `CONTEXT_MANIFEST.md`, `HUMAN_BRIEF.md`, `USER_PREFERENCES.md`, `CURRENT_STATE.md`
""",
    ".contextignore": """.git/
node_modules/
dist/
build/
.cache/
tmp/
*.log
generated/
exports/
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create PM review memory files.")
    parser.add_argument("--path", default=".", help="Project/workspace path.")
    parser.add_argument("--memory-root", default="pm-memory", help="Memory folder name.")
    parser.add_argument("--project-name", default="Untitled PM project")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    memory = root / args.memory_root
    memory.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    for filename, template in TEMPLATES.items():
        target = memory / filename
        if target.exists() and not args.force:
            skipped.append(filename)
            continue
        target.write_text(
            template.format(
                project_name=args.project_name,
                memory_root=args.memory_root,
                timestamp=timestamp,
            ),
            encoding="utf-8",
        )
        created.append(filename)

    print(f"Memory root: {memory}")
    print(f"Created: {len(created)}")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print(f"Skipped existing files: {len(skipped)}")
        for item in skipped:
            print(f"  = {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
