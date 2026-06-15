# Project Memory Templates

Use these templates when initializing or repairing a `project-memory/` workspace.

## Source Design Notes

This skill borrows design patterns from these public repositories without copying their full workflows:

- `JamesShi96/project-butler`: session handoff, update log, project profile, and language adaptation ideas.
- `Frappucc1no/recall-loom`: lean continuity layers, fast vs deep restore, current state plus milestone evidence.
- `tasuku-9/project-memory-skill`: canonical files, capture broadly/promote narrowly, fact/hypothesis separation.
- `fockus/skill-memory-bank`: local memory-bank structure, start/done lifecycle, deterministic scripts for repeatable checks.
- `riponcm/projectmem`: local-first memory, typed records, staleness/search concepts, and CLI/MCP-style retrieval.

PM adaptation:

- Replace coding plans with PRD/strategy review gates.
- Add `REVIEW_LOG.md` for claim audits and draft drift.
- Add `LABEL_AUDIT.md` for labeling consistency and taxonomy problems.
- Add `USER_PREFERENCES.md` for PM working style and review preferences.
- Add `MEMORY_UPDATE_LOG.md` for manual memory refresh traceability.
- Add `MEMORY_LIFECYCLE.md` so stale, superseded, and archived memories do not consume default context.
- Keep `HUMAN_BRIEF.md` as the PM-facing attention surface.

## CONTEXT_MANIFEST.md

```markdown
# Context Manifest

## Project
- Name:
- Owner:
- Memory root: `project-memory/`
- Documentation language:

## Read Order
1. `MEMORY_LIFECYCLE.md`
2. `RECOVERY_NOTES.md`
3. `HUMAN_BRIEF.md`
4. `USER_PREFERENCES.md`
5. `CURRENT_STATE.md`
6. `DECISION_LOG.md`
7. `EVIDENCE_LOG.md`
8. `HYPOTHESIS_LAB.md`
9. `REVIEW_LOG.md`
10. `LABEL_AUDIT.md`
11. `MEMORY_UPDATE_LOG.md`

## Canonical Responsibilities
- User style and review preferences: `USER_PREFERENCES.md`
- Memory lifecycle policy and archive index: `MEMORY_LIFECYCLE.md`
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

## Lifecycle Policy
- Default read statuses: `pinned`, `active`.
- Read `background` only when relevant.
- Do not read `archived`, `superseded`, or `deprecated` by default.
- Do not delete durable memory without explicit user approval.

## Ignore
- `.git/`
- `node_modules/`
- `dist/`
- `build/`
- `.cache/`
- `tmp/`
- generated exports unless explicitly requested
```

## MEMORY_LIFECYCLE.md

```markdown
# Memory Lifecycle

Use this file to keep project memory useful over time. Memory is not append-only: it should be promoted, downgraded, archived, or marked as superseded when the project changes.

## Status Definitions
| Status | Default read? | Meaning |
| --- | --- | --- |
| `pinned` | yes | Durable, high-value context that should stay top of mind. |
| `active` | yes | Current facts, decisions, evidence, assumptions, or risks relevant to ongoing work. |
| `background` | only if relevant | Useful history that should not consume default context. |
| `archived` | no | Historical material kept for traceability or audit. |
| `superseded` | no | Replaced by a newer fact, decision, metric definition, or artifact. |
| `deprecated` | no | Known stale or invalid for current work. |
| `needs_review` | no by default | Candidate for promotion, archive, or deletion; requires human confirmation. |

## Default Read Policy
- Read `pinned` and `active` memory relevant to the task.
- Read `background` memory only when it is semantically relevant or the user asks for history.
- Skip `archived`, `superseded`, and `deprecated` by default.

## Supersession Index
| Old item | Status | Replaced by | Reason | Date |
| --- | --- | --- | --- | --- |

## Archive Index
| Item | Source file | Reason archived | Date | Retrieval notes |
| --- | --- | --- | --- | --- |

## Lifecycle Review Log
### YYYY-MM-DD - Review title
- Trigger/source:
- Kept active:
- Downgraded to background:
- Marked superseded:
- Marked deprecated:
- Archived:
- Needs human review:
```

## USER_PREFERENCES.md

```markdown
# User Preferences

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
```

## CURRENT_STATE.md

```markdown
# Current State

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
```

## DECISION_LOG.md

```markdown
# Decision Log

## YYYY-MM-DD - Decision title
- Status: adopted | rejected | deferred | superseded
- Context:
- Options considered:
- Decision:
- Rationale:
- Risks:
- Revisit when:
- Links to evidence:
```

## EVIDENCE_LOG.md

```markdown
# Evidence Log

## YYYY-MM-DD - Evidence title
- Source:
- Method:
- Finding:
- Confidence: low | medium | high
- Limitations:
- Affects:
- Related hypotheses:
```

## HYPOTHESIS_LAB.md

```markdown
# Hypothesis Lab

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
```

## HUMAN_BRIEF.md

```markdown
# Human Brief

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
```

## REVIEW_LOG.md

```markdown
# Review Log

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
```

## LABEL_AUDIT.md

```markdown
# Label Audit

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
```

## MEMORY_UPDATE_LOG.md

```markdown
# Memory Update Log

Use this log only for manual, user-triggered memory refreshes.

## YYYY-MM-DD HH:MM - Manual update
- Trigger/source:
- Files read:
- Files changed:
- Facts promoted:
- Hypotheses kept open:
- Conflicts or stale items found:
- Lifecycle changes proposed or applied:
- Skipped as not durable:
- Next recommended refresh point:
```

## RECOVERY_NOTES.md

```markdown
# Recovery Notes

## YYYY-MM-DD HH:MM
- What changed:
- What is true now:
- What is blocked:
- Next action:
- Files to read first:
```
