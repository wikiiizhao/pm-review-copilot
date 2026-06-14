---
name: pm-review-copilot
description: PM-focused project memory, manual update workflow, and review-gate system for Agent-assisted PRDs, strategy docs, data insight writeups, and labeling tasks. Use when the user explicitly asks to set up or update durable project memory, resume a PM project across conversations, audit long Agent outputs for hallucination or unsupported claims, compare revised PRD/strategy drafts, identify human-review hotspots, or check consistency across repeated model labeling runs.
---

# PM Review Copilot

Use this skill to move a PM from "read everything the Agent wrote" to "review only the risky, conflicting, or decision-changing parts."

The skill combines project-memory discipline from Project Butler, RecallLoom, project-memory-skill, Memory Bank, and ProjectMem with PM-specific review gates for PRDs, strategy documents, data insights, and labeling workflows.

This skill is not automatic. It does not watch files, run on a schedule, or trigger itself after every Agent response. Use it only when the user explicitly asks to initialize memory, update memory, resume from memory, review an artifact, or audit labels.

## Core Rule

Capture broadly. Promote narrowly. Review by exception.

- Keep durable project facts in files, not chat memory.
- Separate stable facts, decisions, hypotheses, evidence, review findings, and labeling audits.
- Never promote a hypothesis into current truth without evidence, a cited source, or an explicit user decision.
- Do not ask the human to reread the whole artifact when a structured risk report will do.
- Make the review result visually scannable before the detailed tables.
- Respect the user's recorded working style and review preferences when shaping summaries.

## Memory Layout

Prefer a `pm-memory/` directory in the project or document workspace. If that would collide with existing user files, choose `project-memory/` and record the chosen location in `CONTEXT_MANIFEST.md`.

Default files:

- `CONTEXT_MANIFEST.md`: map of memory files, read order, source-of-truth rules, ignore rules.
- `USER_PREFERENCES.md`: PM working style, output preferences, review tolerance, decision style.
- `CURRENT_STATE.md`: confirmed current facts, metrics, constraints, active operating decisions.
- `DECISION_LOG.md`: decisions, rejected options, rationale, risks, revisit conditions.
- `HYPOTHESIS_LAB.md`: unverified ideas, assumptions, possible explanations, unresolved questions.
- `EVIDENCE_LOG.md`: data checks, research findings, source links, methods, limitations.
- `HUMAN_BRIEF.md`: short orientation for the PM; current goal, blockers, risks, next human decision.
- `REVIEW_LOG.md`: PRD/strategy review reports and claim audits.
- `LABEL_AUDIT.md`: labeling consistency audits and label-definition issues.
- `MEMORY_UPDATE_LOG.md`: manual memory refreshes, sources processed, files changed, skipped items.
- `RECOVERY_NOTES.md`: newest-first session handoff.

Use `scripts/init_pm_memory.py` to create this layout.

## Read Order

Read only what the task needs. Do not turn the memory folder into a checklist.

For resume or cross-project work, read in this order:

1. `CONTEXT_MANIFEST.md`
2. `RECOVERY_NOTES.md`
3. `HUMAN_BRIEF.md`
4. `USER_PREFERENCES.md`
5. `CURRENT_STATE.md`
6. latest relevant entries in `DECISION_LOG.md`
7. latest relevant entries in `EVIDENCE_LOG.md`
8. relevant hypotheses in `HYPOTHESIS_LAB.md`
9. latest relevant `REVIEW_LOG.md`, `LABEL_AUDIT.md`, or `MEMORY_UPDATE_LOG.md`

When two project memories are relevant, read both manifests and briefs first, then compare current facts, decisions, metrics, and open questions before drafting.

## Write Routing

Before editing memory files, state a short update plan: which files will change, why, and which relevant files will not be touched. For one obvious file update, one sentence is enough.

Route new information by status:

| Material | Canonical target |
| --- | --- |
| Confirmed current fact, metric definition, constraint, active rule | `CURRENT_STATE.md` |
| Product or strategy decision and rationale | `DECISION_LOG.md` |
| Data check, experiment, user research, source-backed finding | `EVIDENCE_LOG.md` |
| Unverified assumption, open explanation, risky inference | `HYPOTHESIS_LAB.md` |
| Human-facing summary, blocker, next decision | `HUMAN_BRIEF.md` |
| PRD/strategy review result, claim audit, hallucination risk | `REVIEW_LOG.md` |
| Labeling run agreement, disagreement samples, taxonomy issues | `LABEL_AUDIT.md` |
| User working style, output format preference, review tolerance | `USER_PREFERENCES.md` |
| Manual memory refresh summary, processed source list, skipped items | `MEMORY_UPDATE_LOG.md` |
| End-of-session handoff | `RECOVERY_NOTES.md` |

Do not duplicate the same full entry across files. Link or summarize when navigation needs it.

## Promotion Rules

Do not promote anything from `HYPOTHESIS_LAB.md` to `CURRENT_STATE.md` unless at least one condition is true:

- Evidence is recorded in `EVIDENCE_LOG.md`.
- The user explicitly confirms the assumption.
- A decision is recorded in `DECISION_LOG.md`.
- The claim cites an external or internal source supplied in the task.

When promoting, mark the hypothesis as promoted and link the new canonical location.

## User Preference Setup

During initialization, offer the user the `USER_PREFERENCES.md` starter template and ask only for preferences that are relevant to the current work. Do not force a long interview.

Suggested prompt:

```markdown
To make future reviews easier to scan, I can record your PM working preferences. Quick answers are enough:

1. Preferred language and tone:
2. Review style: strict / balanced / speed-first:
3. Output length: concise / standard / detailed:
4. What should always be called out?
5. What can usually be skipped?
6. Decision style: options first / recommendation first / risks first:
7. Formatting preferences:
8. Recurring project context I should remember:
```

Treat these preferences as guidance, not current project truth. Store them in `USER_PREFERENCES.md`, not `CURRENT_STATE.md`.

## Manual Memory Update

Use this workflow when the user asks to "update memory", "refresh pm-memory", "sync today's notes", "把新内容更新到项目 memory", or similar. This workflow is manual and user-triggered.

1. Read `CONTEXT_MANIFEST.md`, `USER_PREFERENCES.md`, `HUMAN_BRIEF.md`, `CURRENT_STATE.md`, and only the logs relevant to the new material.
2. Identify what changed since the last memory update or handoff.
3. State a short update plan: files to edit, files intentionally left untouched, and any claims that will stay as hypotheses.
4. Route each item by status using Write Routing.
5. Append a concise entry to `MEMORY_UPDATE_LOG.md` with:
   - trigger/source
   - files read
   - files changed
   - facts promoted
   - hypotheses kept open
   - conflicts or stale items found
   - next recommended refresh point
6. Refresh `HUMAN_BRIEF.md` when the current goal, blocker, review load, or next human decision changed.
7. Add `RECOVERY_NOTES.md` only when the update creates useful handoff context.

Do not describe this as automatic refresh, background sync, scheduled review, or auto-triggered audit. Say "manual update", "when invoked", or "when the user asks."

## PM Review Gate

Use this gate after the Agent writes or revises a PRD, strategy, data-insight memo, or long plan.

Use exactly one verdict emoji and exactly one review-load emoji at the top. The first line should let the PM understand the result without reading the tables.

Return this structure:

```markdown
## Review Verdict
🟢 Verdict: Pass · Review load: 🟢 Low
One-line summary:

### Verdict Legend
- 🟢 Pass: no known ship blockers; human review can focus on optional polish or local context.
- 🟡 Needs local confirmation: usable direction, but specific claims, assumptions, or decisions need a PM check.
- 🔴 Do not ship: decision-changing risk, conflict, unsupported claim, or missing requirement must be resolved first.

## Must Check
| Priority | Location | Issue | Why it matters | Suggested action |
| --- | --- | --- | --- | --- |

## Claim Audit
| Type | Location | Claim | Evidence status | Risk | Action |
| --- | --- | --- | --- | --- | --- |

## Memory Conflicts
| Location | Draft says | Memory says | Source file | Resolution |
| --- | --- | --- | --- | --- |

## Drift From Previous Version
| Change type | Previous | Current | Risk |
| --- | --- | --- | --- |

## Safe To Ignore
Items reviewed but not worth human attention.
```

Claim types:

- `fact`: stated as true and should be checked.
- `metric`: number, trend, baseline, target, denominator, attribution.
- `causal`: "because", "driven by", "leads to", "therefore".
- `decision`: adopted product/strategy choice.
- `hypothesis`: plausible but unverified assumption.
- `recommendation`: proposed action.

Risk signals:

- no evidence for a decision-changing claim
- conflicts with project memory
- metric denominator or time window missing
- "TBD" rewritten as fact
- old constraint removed silently
- new scope or dependency introduced
- model-generated label definition changes across runs
- conclusion stronger than evidence

## Diff Review

When reviewing a revised document, first compare old vs new. Use `scripts/doc_diff_review.py` for a quick section-level diff when both drafts are plain text or Markdown.

Focus the human on:

- new claims that require evidence
- removed constraints, risks, or open questions
- softened caveats
- changed metric definitions
- changed launch criteria or success metrics
- changed label taxonomy or data inclusion rules

## Labeling Consistency Audit

Use this for repeated model labeling runs or multiple labeler outputs.

If a CSV has one row per sample and multiple label columns, run:

```bash
python3 scripts/label_consistency_audit.py input.csv --id-column id --label-columns label_run_1,label_run_2,label_run_3 --output report.md
```

If `--label-columns` is omitted, the script auto-detects columns containing `label`, `tag`, `class`, or `prediction`.

Then interpret the report for the user:

- exact agreement rate
- per-label disagreement concentration
- samples needing human review
- likely taxonomy boundary problems
- whether the label definition should be revised before more labeling

Prioritize human review for:

- samples with complete disagreement
- labels tied to core metrics or business decisions
- low-frequency but high-impact labels
- pairs of labels that frequently substitute for each other
- rows where the model rationale contradicts the label, if rationales are supplied

## Scripts

- `scripts/init_pm_memory.py`: create the PM memory folder and starter files.
- `scripts/label_consistency_audit.py`: audit repeated labeling runs from CSV.
- `scripts/doc_diff_review.py`: generate a compact Markdown diff between two drafts.

## References

Read `references/pm-memory-templates.md` when you need the exact file templates, review report schema, or source-design notes.

Read `references/source-attribution.md` before publishing or redistributing this skill.

## End Of Session

At a meaningful stopping point during an invoked workflow, offer to update memory if durable project state changed. This is a prompt for user confirmation, not an automatic trigger. If the user already asked to maintain or update memory in this turn, perform the manual update without extra ceremony.

Always consider:

1. Did `CURRENT_STATE.md` change?
2. Was a decision made for `DECISION_LOG.md`?
3. Was evidence added for `EVIDENCE_LOG.md`?
4. Did an assumption belong in `HYPOTHESIS_LAB.md`?
5. Did user preference guidance change in `USER_PREFERENCES.md`?
6. Does `HUMAN_BRIEF.md` need refreshing?
7. Should `MEMORY_UPDATE_LOG.md` record this manual refresh?
8. Should `RECOVERY_NOTES.md` record the next handoff?
