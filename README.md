# PM Review Copilot

语言切换：中文 | [English](docs/README.en.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md)

PM Review Copilot 是一组面向产品经理、适用于 Agent 工作流的项目记忆与审查 skills。

它通过本地持久化项目 memory、结构化审查 Agent 产出的长文档/多轮改动/标注结果，帮助 PM 在多项目、多轮协作中更快发现证据缺口、记忆冲突、幻觉风险和需要人工确认的部分。

本仓库同时提供英文版和中文版：

- `skills/pm-review-copilot`：英文 skill，输出英文。
- `skills/pm-review-copilot-zh`：中文 skill，输出中文。

## Agent 发展趋势

核心判断：Agent 的“产出能力”正在快速增强，但高质量任务的瓶颈会越来越多转移到人的审查、确认和记忆管理上。

| 趋势 | 代表观点 | 对 PM 工作流的影响 |
| --- | --- | --- |
| Agent 从“回答问题”走向“执行任务” | OpenAI 在发布 ChatGPT agent 时提到，Agent 可以使用虚拟计算机在推理和行动之间切换，完成端到端复杂工作流；同时也强调用户仍需要在关键动作前确认、在任务中随时接管，并承认当前 Agent 仍可能出错。参考：[Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)。 | Agent 会产出更多 PRD、策略方案、分析结论和任务结果，人工审核对象从“几段回复”变成“完整交付物”。 |
| 企业组织开始引入人机混合团队 | Microsoft 2025 Work Trend Index 提出，未来组织会走向由人和 Agent 组成的“混合团队”，业务流程会越来越多由 Agent 承担，人类负责设定方向、处理例外和做高判断力决策。报告也提醒，如果 Agent 数量和人的监督能力比例失衡，会带来业务风险和员工过载。参考：[2025: The year the Frontier Firm is born](https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born)。 | 人的角色会更像“审查者、决策者、上下文维护者”，而不是逐字写作的人。 |
| Agent 协作需要新的管理方式 | Microsoft 报告中，Harvard Business School 教授 Karim R. Lakhani 提到，企业可能会出现类似 HR/IT 的 Intelligence Resources 部门，用来管理人与 AI Agent 的协作关系。 | Agent 工作流需要可沉淀、可交接、可审计的项目记忆，而不是只依赖单次对话。 |
| 有效 Agent 应该可调试、可组合 | Anthropic 在工程实践中把 Agent 定义为“由大模型动态决定流程和工具使用方式”的系统，并建议团队从简单、可组合、可调试的模式开始，而不是一味堆复杂框架。参考：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)。 | PM 侧的 Agent 工具也应该把审查逻辑拆成清晰步骤：记忆、证据、冲突、差异和人工确认点。 |

因此，PM Review Copilot 关注的不是“让 Agent 生成更多内容”，而是解决 Agent 工作流里的下一层瓶颈：

- 让项目上下文可以本地持久化，而不是散落在聊天记录里。
- 让长文档审查从逐字阅读变成优先查看风险点。
- 让多轮修改中的事实漂移、约束删除和指标口径变化更容易被发现。
- 让标注一致性问题可以被抽样、排序和定位，而不是完全依赖人工翻查。

## 为什么做这个 skill

作为产品经理，我日常会用 Agent 产品辅助产出 PRD、方案策略、打标数据和数据洞察。使用过程中，我发现真正耗时的往往不是“让 Agent 写出来”，而是持续判断哪些内容可信、哪些内容需要人工确认、哪些改动会改变决策，以及如何让 Agent 在跨项目、跨对话时保留稳定上下文。

常见问题包括：

- PRD、策略方案和分析报告篇幅长，来回修改后，模型容易把假设写成事实，或生成看似合理但缺少证据的结论。
- Agent 回复内容越来越多，人工逐段审核会消耗大量精力，工作一天后尤其容易漏看关键风险。
- 项目很多时，对话通常按项目拆开；一旦项目之间存在交叉，Agent 很难跨对话复用历史记忆、旧约束和已确认决策。
- 草稿迭代时，旧约束、风险、开放问题或发布标准可能被悄悄删除或改写。
- 指标、实验结论和数据洞察可能缺少分母、时间窗口、来源或口径说明。
- “TBD”“待确认”“可能”这类不确定信息，可能在后续版本里被改写成确定事实。
- 多轮模型标注结果不一致，数据量一大，人很难快速定位最值得复核的分歧样本和标签边界问题。

PM Review Copilot 的目标是用工程化方式解决“人在 Agent 工作流中审查效率低”的瓶颈：记录稳定上下文，隔离假设，突出冲突和风险，沉淀人工决策，让人把注意力优先放在真正值得审查的部分。

## 核心能力

| 能力 | 说明 |
| --- | --- |
| 项目记忆初始化 | 创建 `pm-memory/`，包含当前事实、决策、证据、假设、审查日志、标注审查、用户偏好和恢复记录。 |
| 中文/英文双版本 | 英文版用于英文工作流，中文版用于中文 PM 工作流，并默认输出中文模板和报告。 |
| 审查结论可视化 | 审查结果顶部使用 🟢🟡🔴 展示是否通过，以及人工审查负荷高低。 |
| 产品策略审核 | 检查事实、指标、因果、决策、假设和建议是否有证据或与项目记忆冲突。 |
| 版本差异审查 | 对比新旧 PRD/策略草稿，突出新增主张、删除约束、指标定义变化和发布标准变化。 |
| 标注一致性审查 | 审查多轮模型标注或多人标注输出，找出高风险分歧样本和标签边界问题。 |
| 手动记忆更新 | 当用户主动要求时，把新事实、证据、决策、假设和交接信息写入对应 memory 文件。 |
| 用户偏好记录 | 初始化时可记录 PM 的语言、输出长度、审查风格和决策支持偏好。 |

## 安装

不同 Agent 产品对 skills、项目指令、知识库和工具脚本的加载方式不同。本仓库的核心是可复用的 skill 目录，你可以把需要的目录接入任何支持自定义指令/skills/项目知识的 Agent 工作流。

### 通用方式

选择需要的 skill 目录：

- 中文工作流：`skills/pm-review-copilot-zh`
- 英文工作流：`skills/pm-review-copilot`

然后根据你使用的 Agent 产品，把对应目录里的 `SKILL.md` 作为 skill/项目指令加载，并保留同目录下的 `scripts/` 和 `references/`，让 Agent 可以读取说明、调用本地脚本和引用模板。

### Codex 示例

如果你使用 Codex，可以把需要的 skill 目录复制到本地 Codex skills 目录：

```bash
# 中文版
cp -R skills/pm-review-copilot-zh ~/.codex/skills/

# 英文版
cp -R skills/pm-review-copilot ~/.codex/skills/
```

Codex 安装后可以这样调用：

```text
使用 $pm-review-copilot-zh 初始化这个项目的 PM memory。
```

```text
Use $pm-review-copilot to review this PRD for hallucinations, conflicts, and human-check hotspots.
```

## 快速开始

### 1. 初始化项目记忆

中文：

```text
使用 $pm-review-copilot-zh 为这个项目初始化 pm-memory，并询问我必要的偏好设置。
```

英文：

```text
Use $pm-review-copilot to initialize pm-memory for this project and ask only the necessary preference questions.
```

也可以直接运行脚本：

```bash
python3 skills/pm-review-copilot-zh/scripts/init_pm_memory.py --path . --project-name "我的项目"
```

### 2. 审查 PRD 或策略文档

```text
使用 $pm-review-copilot-zh 审查这份 PRD。请重点找出无证据主张、指标口径问题、与 pm-memory 冲突的地方，以及需要我人工确认的内容。
```

输出会包含：

- 顶部视觉结论，例如 `🟡 结论：需要本地确认 · 人工审查负荷：🟡 中`
- 必须检查的项目
- 产品策略审核
- 记忆冲突
- 与上一版的漂移
- 可以忽略的内容

### 3. 手动更新 memory

```text
使用 $pm-review-copilot-zh 把今天讨论的新决策、证据和开放问题更新到 pm-memory。
```

这个 skill 不会自动触发，也不会后台同步。它只在用户主动要求时更新。

### 4. 审查标注一致性

```bash
python3 skills/pm-review-copilot-zh/scripts/label_consistency_audit.py labels.csv \
  --id-column id \
  --label-columns label_run_1,label_run_2,label_run_3 \
  --output label_audit.md
```

## 目录结构

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

## 设计原则

- 广泛采集，择优沉淀，异常审查。
- 把长期事实保存在文件中，不依赖聊天记忆。
- 没有证据、来源或用户决策时，不把假设提升为事实。
- 审查报告优先服务人的注意力，而不是展示 Agent 做了多少工作。
- 明确说明这是手动触发的 skill，不是自动审查或后台同步系统。

## 许可证

本仓库使用 MIT License。来源设计说明见各 skill 下的 `references/source-attribution.md`。
