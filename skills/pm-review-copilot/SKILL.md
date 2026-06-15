---
name: pm-review-copilot
description: PM-focused project memory, memory lifecycle management, manual update workflow, and review-gate system for Agent-assisted PRDs, strategy docs, data insight writeups, and labeling tasks. Use when the user explicitly asks to set up, update, compact, archive, or resume durable project memory, audit long Agent outputs for hallucination or unsupported claims, compare revised PRD/strategy drafts, identify human-review hotspots, or check consistency across repeated model labeling runs.
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
- Treat project memory as a lifecycle, not an append-only dump: keep active memory small, archive stale memory, and preserve traceability.
- Do not ask the human to reread the whole artifact when a structured risk report will do.
- Make the review result visually scannable before the detailed tables.
- Respect the user's recorded working style and review preferences when shaping summaries.

## Memory Layout

Prefer a `project-memory/` directory in the project or document workspace. If an older `pm-memory/` directory already exists, treat it as a legacy memory root and ask before migrating or renaming it. Always record the chosen location in `CONTEXT_MANIFEST.md`.

Default files:

- `CONTEXT_MANIFEST.md`: map of memory files, read order, source-of-truth rules, lifecycle rules, ignore rules.
- `MEMORY_LIFECYCLE.md`: memory status definitions, active read policy, archive/supersession index, lifecycle review log.
- `USER_PREFERENCES.md`: PM working style, output preferences, review tolerance, decision style.
- `CURRENT_STATE.md`: confirmed current facts, metrics, constraints, active operating decisions.
- `DECISION_LOG.md`: decisions, rejected options, rationale, risks, revisit conditions.
- `HYPOTHESIS_LAB.md`: unverified ideas, assumptions, possible explanations, unresolved questions.
- `EVIDENCE_LOG.md`: data checks, research findings, source links, methods, limitations.
- `HUMAN_BRIEF.md`: short orientation for the PM; current goal, blockers, risks, next human decision.
- `REVIEW_LOG.md`: PRD/strategy review reports and claim audits.
- `LABEL_AUDIT.md`: labeling consistency audits and label-definition issues.
- `MEMORY_UPDATE_LOG.md`: manual memory refreshes, sources processed, files changed, lifecycle changes, skipped items.
- `RECOVERY_NOTES.md`: newest-first session handoff.

Use `scripts/init_pm_memory.py` to create this layout.

## Read Order

Read only what the task needs. Do not turn the memory folder into a checklist.

For resume or cross-project work, read in this order:

1. `CONTEXT_MANIFEST.md`
2. `MEMORY_LIFECYCLE.md`
3. `RECOVERY_NOTES.md`
4. `HUMAN_BRIEF.md`
5. `USER_PREFERENCES.md`
6. `CURRENT_STATE.md`
7. latest relevant `pinned` or `active` entries in `DECISION_LOG.md`
8. latest relevant `pinned` or `active` entries in `EVIDENCE_LOG.md`
9. relevant `active` hypotheses in `HYPOTHESIS_LAB.md`
10. latest relevant `REVIEW_LOG.md`, `LABEL_AUDIT.md`, or `MEMORY_UPDATE_LOG.md`

Default read policy:

- Always read `pinned` and `active` memory that is relevant to the task.
- Read `background` memory only when it is semantically relevant or the user asks for history.
- Do not read `archived`, `superseded`, or `deprecated` entries by default; consult them only for audits, disputes, historical reconstruction, or explicit user requests.
- If a file has not adopted lifecycle metadata yet, treat its current-truth sections as `active` and old logs as `background` until the next lifecycle review.

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
| Lifecycle status change, archive index, supersession index, default-read exclusion | `MEMORY_LIFECYCLE.md` |
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

## Memory Lifecycle Management

Use lifecycle management when the user asks to "compact memory", "archive stale memory", "整理 project-memory", "reduce memory bloat", "clean up old memory", or when a manual update finds stale, duplicated, superseded, or no-longer-relevant information.

Lifecycle statuses:

| Status | Default read? | Meaning |
| --- | --- | --- |
| `pinned` | yes | Stable, high-value context that should stay top of mind, such as product principles, hard constraints, key metric definitions, or durable user preferences. |
| `active` | yes | Current facts, decisions, evidence, open assumptions, or risks relevant to ongoing work. |
| `background` | only if relevant | Useful history that can support retrieval, but should not consume default context. |
| `archived` | no | Historical material retained for traceability, audit, or handoff, but not used for current reasoning by default. |
| `superseded` | no | Replaced by a newer fact, decision, metric definition, or artifact. Must link to the replacement. |
| `deprecated` | no | Known stale or invalid for current work. Keep the record, but do not use it as evidence. |
| `needs_review` | no by default | Candidate for promotion, archive, or deletion; requires human confirmation. |

Lifecycle metadata for durable entries:

```yaml
id:
type: fact | decision | evidence | hypothesis | open_question | preference | review_log | label_review
status: pinned | active | background | archived | superseded | deprecated | needs_review
created_at:
updated_at:
last_used_at:
source:
confidence: low | medium | high
valid_from:
valid_until:
superseded_by:
project_phase:
priority: low | medium | high
```

Lifecycle review workflow:

1. Read `CONTEXT_MANIFEST.md`, `MEMORY_LIFECYCLE.md`, `HUMAN_BRIEF.md`, `CURRENT_STATE.md`, and only the logs that may contain stale or duplicated material.
2. Produce a proposed lifecycle change list before editing:
   - keep as `pinned` or `active`
   - downgrade to `background`
   - mark as `superseded`
   - mark as `deprecated`
   - move to `archived`
   - mark as `needs_review`
   - delete only if the user explicitly approves deletion
3. Prefer marking and moving over deleting. PM work often needs historical traceability.
4. Keep `CURRENT_STATE.md` short and current. Move old details into logs or archive sections with links.
5. Update `MEMORY_LIFECYCLE.md` with lifecycle changes, replacements, and default-read exclusions.
6. Append the lifecycle review to `MEMORY_UPDATE_LOG.md`.

Never silently stop using a memory that affects product direction, metrics, launch criteria, compliance, risk, or a user preference. Flag it for human confirmation first.

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

Use this workflow when the user asks to "update memory", "refresh project-memory", "sync today's notes", "把新内容更新到项目 memory", "整理 memory", or similar. This workflow is manual and user-triggered.

1. Read `CONTEXT_MANIFEST.md`, `MEMORY_LIFECYCLE.md`, `USER_PREFERENCES.md`, `HUMAN_BRIEF.md`, `CURRENT_STATE.md`, and only the logs relevant to the new material.
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
   - lifecycle changes proposed or applied
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
- conflicts with `pinned` or `active` project memory
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

- `scripts/init_pm_memory.py`: create the `project-memory/` folder and starter files.
- `scripts/label_consistency_audit.py`: audit repeated labeling runs from CSV.
- `scripts/doc_diff_review.py`: generate a compact Markdown diff between two drafts.

## References

Read `references/project-memory-templates.md` when you need the exact file templates, review report schema, or source-design notes.

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
9. Should stale, duplicated, or superseded memory be proposed for lifecycle review?
