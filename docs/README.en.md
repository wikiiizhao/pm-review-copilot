# PM Review Copilot

Language: [中文](../README.md) | English | [日本語](README.ja.md) | [한국어](README.ko.md)

PM Review Copilot is a set of project-memory and review skills for product managers working with agent workflows.

It helps PMs persist project memory locally and systematically review long agent-generated documents, multi-round revisions, and labeling outputs, so they can spot evidence gaps, memory conflicts, hallucination risks, and items that need human confirmation faster across multiple projects and collaboration rounds.

This repository includes English and Chinese skills:

- `skills/pm-review-copilot`: English skill with English outputs.
- `skills/pm-review-copilot-zh`: Chinese skill with Chinese outputs.

## Agent Trends

Core view: Agents are getting much stronger at producing work, but the bottleneck for high-quality tasks is increasingly shifting to human review, confirmation, and memory management.

| Trend | Representative view | Impact on PM workflows |
| --- | --- | --- |
| Agents are moving from answering questions to executing tasks | When introducing ChatGPT agent, OpenAI described an agent that can use a virtual computer, switch between reasoning and action, and complete end-to-end workflows. OpenAI also emphasized that users still need to confirm key actions, take over at any time, and account for the fact that agents can still make mistakes. See [Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/). | Agents will produce more PRDs, strategy docs, analysis, and task outputs. Human review shifts from checking a few paragraphs to reviewing full deliverables. |
| Companies are starting to organize around human-agent teams | Microsoft 2025 Work Trend Index describes a shift toward "hybrid teams" of people and agents, where agents take on more business processes while humans set direction, handle exceptions, and make judgment-heavy decisions. It also warns that a poor ratio between agent volume and human supervision capacity can create business risk and overload. See [2025: The year the Frontier Firm is born](https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born). | The human role becomes closer to reviewer, decision-maker, and context steward, not just the person writing every line. |
| Agent collaboration needs new management patterns | In Microsoft's report, Harvard Business School professor Karim R. Lakhani suggests that companies may create Intelligence Resources functions, similar to HR or IT, to manage how people and AI agents work together. | Agent workflows need project memory that can be persisted, handed off, and reviewed, instead of relying only on a single chat thread. |
| Effective agents should be debuggable and composable | Anthropic describes agents as systems where LLMs dynamically direct their own process and tool usage, and recommends starting with simple, composable, debuggable patterns instead of piling on complex frameworks. See [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents). | PM-facing agent tools should also break review into clear steps: memory, evidence, conflicts, diffs, and human confirmation points. |

PM Review Copilot is therefore less about making agents generate more content, and more about the next bottleneck in agent workflows:

- Make project context durable locally instead of scattered across chat history.
- Turn long-document review from line-by-line reading into risk-first review.
- Make factual drift, removed constraints, and metric-definition changes easier to catch across revisions.
- Make labeling consistency issues easier to sample, prioritize, and locate instead of relying on manual inspection alone.

## Why This Skill Exists

As a product manager, I use agent products in daily work to draft PRDs, strategy plans, labeling data, and data-insight writeups. The hard part is often not getting the agent to write something. It is continuously deciding what can be trusted, what needs human confirmation, which changes affect decisions, and how to keep stable context when agents work across projects and chat threads.

Common pain points include:

- PRDs, strategy plans, and analysis reports are long. After several revision rounds, models can turn assumptions into facts or produce plausible conclusions without enough evidence.
- Agent responses keep getting longer, and reviewing them paragraph by paragraph consumes a lot of energy, especially late in the workday when key risks are easier to miss.
- When many projects are split across separate conversations, agents struggle to reuse historical memory, old constraints, and confirmed decisions across related projects.
- During draft iteration, old constraints, risks, open questions, or launch criteria can be quietly removed or rewritten.
- Metrics, experiment conclusions, and data insights may lack denominators, time windows, sources, or definition details.
- Uncertain language such as "TBD," "to confirm," or "possible" may later be rewritten as settled fact.
- Repeated model-labeling runs can be inconsistent. When the dataset is large, it is hard for humans to quickly locate the disagreement samples and taxonomy boundaries most worth reviewing.

PM Review Copilot aims to address the bottleneck of low human review efficiency in agent workflows through an engineering-style approach: preserve stable context, isolate assumptions, surface conflicts and risks, record human decisions, and help people spend attention on the parts that most deserve review.

## Core Capabilities

| Capability | Description |
| --- | --- |
| Project memory setup | Creates `pm-memory/` with current facts, decisions, evidence, hypotheses, review logs, labeling reviews, user preferences, and handoff notes. |
| English and Chinese skills | Use the English skill for English workflows and the Chinese skill for Chinese PM workflows with Chinese templates and reports by default. |
| Visual review verdict | Uses 🟢🟡🔴 at the top of review outputs to show whether the work passes and how heavy the human review load is. |
| Product strategy review | Checks whether facts, metrics, causality, decisions, hypotheses, and recommendations are supported by evidence or conflict with project memory. |
| Revision diff review | Compares old and new PRD or strategy drafts, highlighting new assertions, removed constraints, metric-definition changes, and launch-criteria changes. |
| Labeling consistency review | Reviews repeated model-labeling or multi-rater outputs to find high-risk disagreement samples and taxonomy boundary issues. |
| Manual memory update | Writes new facts, evidence, decisions, assumptions, and handoff notes to the right memory files only when the user explicitly asks. |
| User preference capture | Records language, output length, review style, and decision-support preferences during setup. |

## Installation

Different agent products load skills, project instructions, knowledge bases, and local scripts in different ways. The reusable unit in this repository is the skill directory, which can be connected to any agent workflow that supports custom instructions, skills, or project knowledge.

### General Setup

Choose the skill directory you need:

- Chinese workflow: `skills/pm-review-copilot-zh`
- English workflow: `skills/pm-review-copilot`

Then load the corresponding `SKILL.md` as a skill or project instruction in your agent product, and keep the sibling `scripts/` and `references/` directories available so the agent can read guidance, call local scripts, and reuse templates.

### Codex Example

If you use Codex, copy the skill directory you need into your local Codex skills directory:

```bash
# Chinese
cp -R skills/pm-review-copilot-zh ~/.codex/skills/

# English
cp -R skills/pm-review-copilot ~/.codex/skills/
```

After installing in Codex, you can invoke it like this:

```text
Use $pm-review-copilot to initialize pm-memory for this project.
```

```text
使用 $pm-review-copilot-zh 初始化这个项目的 PM memory。
```

## Quick Start

### 1. Initialize Project Memory

English:

```text
Use $pm-review-copilot to initialize pm-memory for this project and ask only the necessary preference questions.
```

Chinese:

```text
使用 $pm-review-copilot-zh 为这个项目初始化 pm-memory，并询问我必要的偏好设置。
```

You can also run the script directly:

```bash
python3 skills/pm-review-copilot/scripts/init_pm_memory.py --path . --project-name "My Project"
```

### 2. Review a PRD or Strategy Document

```text
Use $pm-review-copilot to review this PRD. Focus on unsupported assertions, metric-definition issues, conflicts with pm-memory, and items that require my confirmation.
```

The output includes:

- A visual verdict at the top, for example `🟡 Verdict: needs local confirmation · Human review load: 🟡 medium`
- Must-check items
- Product strategy review
- Memory conflicts
- Drift from the previous version
- Items that can be safely ignored

### 3. Manually Update Memory

```text
Use $pm-review-copilot to update pm-memory with today's new decisions, evidence, and open questions.
```

This skill does not run automatically and does not sync in the background. It updates memory only when the user explicitly asks.

### 4. Review Labeling Consistency

```bash
python3 skills/pm-review-copilot/scripts/label_consistency_audit.py labels.csv \
  --id-column id \
  --label-columns label_run_1,label_run_2,label_run_3 \
  --output label_audit.md
```

## Directory Structure

```text
.
├── skills/
│   ├── pm-review-copilot/
│   └── pm-review-copilot-zh/
├── docs/
│   ├── README.en.md
│   ├── README.ja.md
│   └── README.ko.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Design Principles

- Collect broadly, preserve selectively, and review exceptions.
- Store long-lived facts in files instead of relying on chat memory.
- Do not promote assumptions into facts without evidence, sources, or user decisions.
- Optimize review reports for human attention, not for showing how much work the agent did.
- Make it explicit that this is a manually triggered skill, not an automatic review or background sync system.

## License

This repository uses the MIT License. See each skill's `references/source-attribution.md` for design lineage.
