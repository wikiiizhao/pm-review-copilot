# Source Attribution

This skill is an original PM-focused adaptation built after reviewing public project-memory and agent-continuity projects. It does not vendor their source code, helper scripts, or full documentation. It adapts general workflow ideas such as file-based project memory, current-state summaries, decision logs, handoff notes, evidence logs, and consistency checks.

## Referenced Projects

| Project | Repository | What informed this skill |
| --- | --- | --- |
| Project Butler | https://github.com/JamesShi96/project-butler | Session handoff, project profile, update-log, language-adaptation, and file-template organization. |
| RecallLoom | https://github.com/Frappucc1no/recall-loom | Lightweight continuity layers, fast/deep resume behavior, current-state summaries, and milestone evidence separation. |
| project-memory-skill | https://github.com/tasuku-9/project-memory-skill | Canonical memory files, fact/hypothesis separation, capture broadly/promote narrowly discipline, and conflict-routing ideas. |
| Memory Bank Skill | https://github.com/fockus/skill-memory-bank | Local memory-bank lifecycle, agent-agnostic structure, and deterministic helper-script philosophy. |
| ProjectMem | https://github.com/riponcm/projectmem | Local-first memory, typed project records, staleness/search concepts, and MCP/CLI retrieval ideas. |

## Reuse Boundary

- No upstream source code is copied into this skill.
- No upstream complete documentation files are copied into this skill.
- File names such as `CURRENT_STATE.md`, `DECISION_LOG.md`, and `RECOVERY_NOTES.md` are treated as generic project-memory conventions.
- Short terminology and workflow concepts are attributed here to make the design lineage clear.

## Publishing Guidance

Before publishing this skill as a public repository:

1. Add your own repository license, such as MIT or Apache-2.0, if you want others to reuse it.
2. Keep this attribution file in the published repository.
3. If future versions copy upstream code, scripts, or substantial text, include the required upstream license text and notices for that copied material.
4. Re-check each referenced repository's current license before publishing a derivative that copies any expression from it.
