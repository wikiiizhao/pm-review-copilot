---
name: pm-review-copilot-zh
description: 面向产品经理的项目记忆、记忆生命周期管理、手动更新和审查关卡工作流，适用于 Agent 辅助生成的 PRD、策略文档、数据洞察、长方案和标注任务。Use when the user explicitly asks in Chinese or requests Chinese output to initialize, update, compact, archive, or resume durable project memory, review long Agent outputs for hallucinations or unsupported claims, compare revised PRD/strategy drafts, identify human-review hotspots, or audit labeling consistency. 所有面向用户的总结、审查结论、模板和脚本报告都应使用中文输出。
---

# PM Review Copilot 中文版

使用这个 skill，把产品经理从“通读 Agent 写出的所有内容”转向“只审查高风险、冲突、会影响决策的部分”。

这个 skill 结合项目记忆方法和产品经理常见审查场景：PRD、策略文档、数据洞察、长计划、标注任务和多轮版本对比。

这个 skill 不会自动触发。它不会监听文件、定时运行，也不会在每次 Agent 回复后自行审查。只有在用户明确要求初始化记忆、更新记忆、整理记忆、归档记忆、从记忆恢复项目、审查文档或审查标注时才使用。

## 核心规则

广泛采集，择优沉淀，异常审查。

- 将长期项目事实保存在文件中，不依赖聊天记忆。
- 区分稳定事实、决策、假设、证据、审查发现和标注审查。
- 没有证据、来源或用户明确决策时，不要把假设提升为当前事实。
- 将项目记忆视为生命周期，而不是无限追加的记录堆：保持当前记忆精简，归档过时记忆，并保留可追溯性。
- 不要要求人重新通读整篇产物；用结构化风险报告聚焦需要人工判断的部分。
- 审查结果必须先给出一眼可见的视觉摘要，再给细表。
- 输出风格要尊重 `USER_PREFERENCES.md` 中记录的使用者偏好。
- 所有面向用户的输出使用中文。

## 记忆目录

优先在项目或文档工作区中使用 `project-memory/` 目录。如果已经存在旧版 `pm-memory/`，将其视为历史记忆目录；迁移或重命名前必须先询问用户。始终在 `CONTEXT_MANIFEST.md` 中记录实际使用的目录。

默认文件：

- `CONTEXT_MANIFEST.md`：记忆文件地图、读取顺序、事实来源规则、生命周期规则、忽略规则。
- `MEMORY_LIFECYCLE.md`：记忆状态定义、默认读取策略、归档/替代索引、生命周期整理记录。
- `USER_PREFERENCES.md`：产品经理的工作风格、输出偏好、审查容忍度、决策风格。
- `CURRENT_STATE.md`：已确认的当前事实、指标、约束、有效决策。
- `DECISION_LOG.md`：决策、被否方案、理由、风险、复盘条件。
- `HYPOTHESIS_LAB.md`：未经验证的想法、假设、可能解释、未解问题。
- `EVIDENCE_LOG.md`：数据检查、研究发现、来源链接、方法和限制。
- `HUMAN_BRIEF.md`：给 PM 的短摘要；当前目标、阻塞、风险、下一步人工决策。
- `REVIEW_LOG.md`：PRD/策略审查报告和 claim audit。
- `LABEL_AUDIT.md`：标注一致性审查和标签定义问题。
- `MEMORY_UPDATE_LOG.md`：手动记忆刷新记录、处理来源、变更文件、生命周期变更、跳过项。
- `RECOVERY_NOTES.md`：按时间倒序的会话交接记录。

使用 `scripts/init_pm_memory.py` 创建这套目录。

## 读取顺序

只读取任务需要的文件，不要把记忆目录变成机械清单。

恢复项目或跨项目工作时，按这个顺序读取：

1. `CONTEXT_MANIFEST.md`
2. `MEMORY_LIFECYCLE.md`
3. `RECOVERY_NOTES.md`
4. `HUMAN_BRIEF.md`
5. `USER_PREFERENCES.md`
6. `CURRENT_STATE.md`
7. `DECISION_LOG.md` 中最新且相关的 `pinned` 或 `active` 条目
8. `EVIDENCE_LOG.md` 中最新且相关的 `pinned` 或 `active` 条目
9. `HYPOTHESIS_LAB.md` 中相关且 `active` 的假设
10. 最新且相关的 `REVIEW_LOG.md`、`LABEL_AUDIT.md` 或 `MEMORY_UPDATE_LOG.md`

默认读取策略：

- 默认读取与任务相关的 `pinned` 和 `active` 记忆。
- 只有在语义相关或用户要求追溯历史时，才读取 `background` 记忆。
- 默认不读取 `archived`、`superseded`、`deprecated` 条目；只有在审计、争议处理、历史复盘或用户明确要求时才查阅。
- 如果旧文件还没有生命周期 metadata，先把当前事实区视为 `active`，旧日志视为 `background`，等下一次生命周期整理时再补状态。

如果两个项目记忆都相关，先读两个 manifest 和 brief，再比较当前事实、决策、指标和开放问题。

## 写入路由

编辑记忆文件前，先说明简短更新计划：会改哪些文件、为什么改、哪些相关文件不会动。只有一个明显文件要改时，一句话即可。

按信息状态写入：

| 信息类型 | 规范目标 |
| --- | --- |
| 已确认的当前事实、指标定义、约束、有效规则 | `CURRENT_STATE.md` |
| 产品或策略决策及理由 | `DECISION_LOG.md` |
| 数据检查、实验、用户研究、带来源发现 | `EVIDENCE_LOG.md` |
| 未验证假设、开放解释、风险推断 | `HYPOTHESIS_LAB.md` |
| 给人的摘要、阻塞、下一步决策 | `HUMAN_BRIEF.md` |
| PRD/策略审查结果、claim audit、幻觉风险 | `REVIEW_LOG.md` |
| 标注运行一致性、分歧样本、标签体系问题 | `LABEL_AUDIT.md` |
| 用户工作风格、输出格式偏好、审查容忍度 | `USER_PREFERENCES.md` |
| 生命周期状态变更、归档索引、替代关系索引、默认读取排除项 | `MEMORY_LIFECYCLE.md` |
| 手动记忆刷新摘要、处理来源列表、跳过项 | `MEMORY_UPDATE_LOG.md` |
| 会话结束交接 | `RECOVERY_NOTES.md` |

不要把同一个完整条目重复写进多个文件。需要导航时，用链接或短摘要。

## 提升规则

除非满足至少一个条件，否则不要把 `HYPOTHESIS_LAB.md` 中的内容提升到 `CURRENT_STATE.md`：

- 证据已记录在 `EVIDENCE_LOG.md`。
- 用户明确确认该假设。
- 决策已记录在 `DECISION_LOG.md`。
- 该 claim 引用了任务中提供的外部或内部来源。

提升时，标记原假设为已提升，并链接新的规范位置。

## 记忆生命周期管理

当用户要求“整理 memory”“整理 project-memory”“压缩记忆”“归档过时记忆”“清理旧记忆”，或手动更新时发现过时、重复、已被替代、不再相关的信息时，使用这个机制。

记忆状态：

| 状态 | 默认读取？ | 含义 |
| --- | --- | --- |
| `pinned` | 是 | 长期高价值上下文，例如产品原则、硬约束、关键指标定义、稳定用户偏好。 |
| `active` | 是 | 当前工作相关的事实、决策、证据、开放假设或风险。 |
| `background` | 仅相关时 | 有历史价值，可支持检索，但不应默认占用上下文。 |
| `archived` | 否 | 为追溯、审计或交接保留的历史材料，默认不参与当前推理。 |
| `superseded` | 否 | 已被新的事实、决策、指标定义或产物替代，必须链接替代项。 |
| `deprecated` | 否 | 已知过时或对当前工作无效，保留记录但不能作为证据使用。 |
| `needs_review` | 默认否 | 需要人工确认是保留、降权、归档还是删除的候选项。 |

长期条目的 lifecycle metadata：

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

生命周期整理流程：

1. 读取 `CONTEXT_MANIFEST.md`、`MEMORY_LIFECYCLE.md`、`HUMAN_BRIEF.md`、`CURRENT_STATE.md`，以及可能包含过时或重复内容的相关日志。
2. 修改前先给出建议清单：
   - 保持为 `pinned` 或 `active`
   - 降为 `background`
   - 标记为 `superseded`
   - 标记为 `deprecated`
   - 移入 `archived`
   - 标记为 `needs_review`
   - 只有用户明确同意时才删除
3. 优先“标记和移动”，不要直接删除。PM 工作经常需要历史可追溯。
4. 保持 `CURRENT_STATE.md` 精简且当前有效。旧细节移入日志或归档区，并保留链接。
5. 在 `MEMORY_LIFECYCLE.md` 中记录生命周期变更、替代关系和默认不读取的排除项。
6. 在 `MEMORY_UPDATE_LOG.md` 中追加这次生命周期整理记录。

凡是影响产品方向、指标口径、发布标准、合规风险或用户偏好的记忆，都不要静默停用；必须先标记为需要人工确认。

## 用户偏好设置

初始化时，向用户提供 `USER_PREFERENCES.md` 的启动模板，只询问当前工作真正需要的偏好。不要强迫用户完成长访谈。

建议提问：

```markdown
为了让之后的审查更好扫读，我可以记录你的 PM 工作偏好。简单回答即可：

1. 偏好的语言和语气：
2. 审查风格：严格 / 平衡 / 速度优先：
3. 输出长度：简洁 / 标准 / 详细：
4. 哪些内容必须始终提醒？
5. 哪些内容通常可以跳过？
6. 决策支持风格：先给选项 / 先给建议 / 先讲风险：
7. 格式偏好：
8. 希望长期记住的项目背景：
```

将这些偏好视为输出指导，而不是项目事实。写入 `USER_PREFERENCES.md`，不要写入 `CURRENT_STATE.md`。

## 手动记忆更新

当用户说“更新 memory”“刷新 project-memory”“同步今天的信息”“把新内容更新到项目 memory”“整理 memory”等类似请求时，使用这个工作流。该流程是手动、由用户触发的。

1. 读取 `CONTEXT_MANIFEST.md`、`MEMORY_LIFECYCLE.md`、`USER_PREFERENCES.md`、`HUMAN_BRIEF.md`、`CURRENT_STATE.md`，以及与新材料相关的日志。
2. 识别自上次记忆更新或交接以来发生了什么变化。
3. 说明简短更新计划：要编辑的文件、明确不动的文件、哪些 claim 会保留为假设。
4. 按“写入路由”处理每条信息。
5. 在 `MEMORY_UPDATE_LOG.md` 追加简短记录，包含：
   - 触发方式/来源
   - 已读取文件
   - 已修改文件
   - 已提升事实
   - 仍保留的假设
   - 发现的冲突或过期信息
   - 已建议或已执行的生命周期变更
   - 下一次建议刷新时点
6. 当前目标、阻塞、审查负荷或下一步人工决策变化时，刷新 `HUMAN_BRIEF.md`。
7. 只有当更新产生有用交接上下文时，才写 `RECOVERY_NOTES.md`。

不要把它描述为自动刷新、后台同步、定时审查或自动触发审计。使用“手动更新”“被调用时”“当用户要求时”等中性表述。

## PM 审查关卡

当 Agent 写出或修改 PRD、策略、数据洞察备忘录或长计划后，使用这个审查关卡。

顶部只能使用一个 verdict emoji 和一个 review-load emoji。第一行要让 PM 不读表格也能理解审查结果。

返回结构：

```markdown
## 审查结论
🟢 结论：通过 · 人工审查负荷：🟢 低
一句话总结：

### 图例
- 🟢 通过：没有已知阻塞，人工审查可聚焦在润色或本地上下文。
- 🟡 需要本地确认：方向可用，但部分 claim、假设或决策需要 PM 确认。
- 🔴 不建议发布：存在影响决策的风险、冲突、无证据 claim 或缺失要求，需要先解决。

## 必须检查
| 优先级 | 位置 | 问题 | 为什么重要 | 建议动作 |
| --- | --- | --- | --- | --- |

## Claim 审计
| 类型 | 位置 | Claim | 证据状态 | 风险 | 动作 |
| --- | --- | --- | --- | --- | --- |

## 记忆冲突
| 位置 | 草稿说法 | 记忆记录 | 来源文件 | 解决方式 |
| --- | --- | --- | --- | --- |

## 与上一版的漂移
| 变化类型 | 上一版 | 当前版 | 风险 |
| --- | --- | --- | --- |

## 可以忽略
已经检查但不值得人工投入注意力的内容。
```

Claim 类型：

- `fact`：被当作事实陈述，应检查。
- `metric`：数字、趋势、基线、目标、分母、归因。
- `causal`：包含“因为”“由...驱动”“导致”“因此”等因果关系。
- `decision`：已采纳的产品或策略选择。
- `hypothesis`：合理但未经验证的假设。
- `recommendation`：建议采取的行动。

风险信号：

- 会影响决策的 claim 没有证据
- 与 `pinned` 或 `active` 项目记忆冲突
- 指标缺少分母或时间窗口
- “TBD” 被改写成事实
- 旧约束被静默删除
- 引入了新范围或新依赖
- 模型生成的标签定义在多轮中变化
- 结论强于证据

## Diff 审查

审查修改版文档时，先比较新旧版本。两个草稿都是纯文本或 Markdown 时，可使用 `scripts/doc_diff_review.py` 生成简短的段落级 diff。

重点让人检查：

- 新增且需要证据的 claim
- 被删除的约束、风险、开放问题和 caveat
- 被弱化的保留意见
- 变化的指标定义
- 变化的发布标准或成功指标
- 变化的标签体系或数据纳入规则

## 标注一致性审查

用于多轮模型标注或多个标注者输出。

如果 CSV 每行是一个样本，且有多个标签列，运行：

```bash
python3 scripts/label_consistency_audit.py input.csv --id-column id --label-columns label_run_1,label_run_2,label_run_3 --output report.md
```

如果省略 `--label-columns`，脚本会自动检测列名中包含 `label`、`tag`、`class` 或 `prediction` 的列。

然后用中文向用户解释报告：

- 完全一致率
- 分歧集中在哪些标签
- 需要人工审查的样本
- 可能的标签边界问题
- 是否应在继续标注前修订标签定义

优先让人审查：

- 完全分歧的样本
- 与核心指标或业务决策相关的标签
- 低频但高影响标签
- 经常互相替代的一组标签
- 如果提供了理由，标签和理由互相矛盾的行

## 脚本

- `scripts/init_pm_memory.py`：创建中文 `project-memory/` 文件夹和启动文件。
- `scripts/label_consistency_audit.py`：审查 CSV 中重复标注的一致性，并输出中文 Markdown 报告。
- `scripts/doc_diff_review.py`：比较两个草稿，生成中文 Markdown diff 报告。

## 参考文件

需要精确文件模板、审查报告 schema 或来源设计说明时，读取 `references/project-memory-templates.md`。

发布或再分发这个 skill 前，读取 `references/source-attribution.md`。

## 会话结束

在已调用的工作流进入有意义的停止点时，如果长期项目状态发生变化，询问是否更新记忆。这是向用户确认，不是自动触发。如果用户在本轮已经要求维护或更新记忆，则直接执行手动更新。

始终考虑：

1. `CURRENT_STATE.md` 是否变化？
2. 是否有决策要写入 `DECISION_LOG.md`？
3. 是否有证据要写入 `EVIDENCE_LOG.md`？
4. 是否有假设属于 `HYPOTHESIS_LAB.md`？
5. `USER_PREFERENCES.md` 中的偏好是否变化？
6. `HUMAN_BRIEF.md` 是否需要刷新？
7. `MEMORY_UPDATE_LOG.md` 是否应记录这次手动刷新？
8. `RECOVERY_NOTES.md` 是否应记录下一次交接？
9. 是否需要把过时、重复或已被替代的记忆纳入生命周期整理建议？
