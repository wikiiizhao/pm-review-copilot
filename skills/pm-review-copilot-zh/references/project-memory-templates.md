# 项目记忆模板

初始化或修复 `project-memory/` 工作区时使用这些模板。

## 来源设计说明

这个 skill 借鉴了若干公开项目的设计模式，但没有复制它们的完整工作流：

- `JamesShi96/project-butler`：会话交接、更新日志、项目档案、语言适配。
- `Frappucc1no/recall-loom`：轻量连续性层、快速/深度恢复、当前状态加里程碑证据。
- `tasuku-9/project-memory-skill`：规范文件、广泛捕捉/谨慎提升、事实和假设分离。
- `fockus/skill-memory-bank`：本地 memory bank 结构、开始/完成生命周期、可重复检查脚本。
- `riponcm/projectmem`：本地优先记忆、类型化记录、陈旧度和检索概念。

PM 适配：

- 用 PRD/策略审查关卡替代代码计划。
- 增加 `REVIEW_LOG.md` 记录 claim audit 和版本漂移。
- 增加 `LABEL_AUDIT.md` 记录标注一致性和标签体系问题。
- 增加 `USER_PREFERENCES.md` 记录 PM 工作风格和审查偏好。
- 增加 `MEMORY_UPDATE_LOG.md` 记录手动记忆刷新。
- 增加 `MEMORY_LIFECYCLE.md`，避免过时、已替代、已归档的记忆继续占用默认上下文。
- 保留 `HUMAN_BRIEF.md` 作为 PM 的注意力界面。

## CONTEXT_MANIFEST.md

```markdown
# 上下文清单

## 项目
- 名称：
- 负责人：
- 记忆目录：`project-memory/`
- 文档语言：中文

## 读取顺序
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

## 规范职责
- 用户风格和审查偏好：`USER_PREFERENCES.md`
- 记忆生命周期策略和归档索引：`MEMORY_LIFECYCLE.md`
- 当前事实：`CURRENT_STATE.md`
- 决策和理由：`DECISION_LOG.md`
- 证据和来源检查：`EVIDENCE_LOG.md`
- 未验证想法：`HYPOTHESIS_LAB.md`
- 人类审查界面：`HUMAN_BRIEF.md`
- PRD/策略审查历史：`REVIEW_LOG.md`
- 标注审计历史：`LABEL_AUDIT.md`
- 手动记忆刷新历史：`MEMORY_UPDATE_LOG.md`
- 恢复交接：`RECOVERY_NOTES.md`

## 冲突处理规则
当前事实冲突时，按以下优先级处理：
1. `CURRENT_STATE.md`
2. 最新且相关的 `DECISION_LOG.md`
3. 最新且相关的 `EVIDENCE_LOG.md`
4. 最新的 `RECOVERY_NOTES.md`
5. `HUMAN_BRIEF.md`
6. `HYPOTHESIS_LAB.md`

合并冲突前先报告。

## 生命周期规则
- 默认读取状态：`pinned`、`active`。
- 只有相关时才读取 `background`。
- 默认不读取 `archived`、`superseded`、`deprecated`。
- 未经用户明确同意，不删除长期记忆。

## 忽略
- `.git/`
- `node_modules/`
- `dist/`
- `build/`
- `.cache/`
- `tmp/`
- 生成导出物，除非用户明确要求
```

## MEMORY_LIFECYCLE.md

```markdown
# 记忆生命周期

这个文件用于让项目记忆长期保持可用。记忆不是无限追加的记录堆：随着项目变化，旧记忆应该被提升、降权、归档或标记为已被替代。

## 状态定义
| 状态 | 默认读取？ | 含义 |
| --- | --- | --- |
| `pinned` | 是 | 长期高价值上下文，应始终优先考虑。 |
| `active` | 是 | 当前工作相关的事实、决策、证据、假设或风险。 |
| `background` | 仅相关时 | 有历史价值，但不应默认占用上下文。 |
| `archived` | 否 | 为追溯或审计保留的历史材料。 |
| `superseded` | 否 | 已被新的事实、决策、指标定义或产物替代。 |
| `deprecated` | 否 | 已知过时或对当前工作无效。 |
| `needs_review` | 默认否 | 需要人工确认是保留、归档还是删除。 |

## 默认读取策略
- 读取与任务相关的 `pinned` 和 `active` 记忆。
- 只有语义相关或用户要求追溯历史时，才读取 `background` 记忆。
- 默认跳过 `archived`、`superseded`、`deprecated`。

## 替代关系索引
| 旧条目 | 状态 | 替代项 | 原因 | 日期 |
| --- | --- | --- | --- | --- |

## 归档索引
| 条目 | 来源文件 | 归档原因 | 日期 | 检索说明 |
| --- | --- | --- | --- | --- |

## 生命周期整理记录
### YYYY-MM-DD - 整理标题
- 触发方式/来源：
- 保持 active：
- 降为 background：
- 标记 superseded：
- 标记 deprecated：
- 已归档：
- 需要人工确认：
```

## USER_PREFERENCES.md

```markdown
# 用户偏好

这个文件用于记录 PM 的工作偏好。不要把偏好当作项目事实。

## 快速设置问题
只回答当前重要的部分即可。

1. 偏好的语言和语气：
2. 审查风格：严格 | 平衡 | 速度优先
3. 输出长度：简洁 | 标准 | 详细
4. 哪些内容必须始终提醒？
5. 哪些内容通常可以跳过？
6. 决策支持风格：先给选项 | 先给建议 | 先讲风险
7. 格式偏好：
8. 希望长期记住的项目背景：

## 当前偏好
- 语言：
- 语气：
- 审查严格度：
- 偏好的摘要形态：
- 表格：是 | 否 | 仅审计时使用
- 视觉结论：是 | 否
- 人工审查容忍度：
- 始终提醒：
- 通常跳过：
- 决策支持风格：

## 使用中学到的偏好
| 日期 | 学到的偏好 | 来源 |
| --- | --- | --- |
```

## CURRENT_STATE.md

```markdown
# 当前状态

## 稳定事实
- 

## 指标和定义
| 指标 | 定义 | 来源 | 最后确认时间 | 备注 |
| --- | --- | --- | --- | --- |

## 当前有效决策
- 

## 当前上下文
- 当前目标：
- 当前阶段：
- 主要阻塞：
- 下一步人工决策：

## 约束
- 

## 已废弃或退休
| 项目 | 替代项 | 原因 | 日期 |
| --- | --- | --- | --- |
```

## DECISION_LOG.md

```markdown
# 决策日志

## YYYY-MM-DD - 决策标题
- 状态：已采纳 | 已拒绝 | 延后 | 已被替代
- 背景：
- 考虑过的选项：
- 决策：
- 理由：
- 风险：
- 复盘条件：
- 证据链接：
```

## EVIDENCE_LOG.md

```markdown
# 证据日志

## YYYY-MM-DD - 证据标题
- 来源：
- 方法：
- 发现：
- 置信度：低 | 中 | 高
- 限制：
- 影响：
- 相关假设：
```

## HYPOTHESIS_LAB.md

```markdown
# 假设实验室

## 原始想法
- [ ] 假设：
  - 为什么重要：
  - 如何验证：

## 工作假设
### HYP-001 - 标题
- 状态：开放 | 验证中 | 已提升 | 已放弃
- Claim：
- 所需证据：
- 反对意见：
- 复盘条件：
```

## HUMAN_BRIEF.md

```markdown
# 人类简报

## 注意力摘要
- 当前目标：
- 最大风险：
- 下一步决策：
- 审查负荷：低 | 中 | 高

## 跟踪事项
| 事项 | 状态 | 下一步动作或阻塞 | 来源 |
| --- | --- | --- | --- |

## 必须检查
- 

## 最近变化
- 
```

## REVIEW_LOG.md

```markdown
# 审查日志

## YYYY-MM-DD - 产物标题
- 产物：
- 结论：🟢 通过 | 🟡 需要本地确认 | 🔴 不建议发布
- 人工审查负荷：🟢 低 | 🟡 中 | 🔴 高
- 一句话总结：

### 必须检查
| 优先级 | 位置 | 问题 | 为什么重要 | 建议动作 |
| --- | --- | --- | --- | --- |

### Claim 审计
| 类型 | 位置 | Claim | 证据状态 | 风险 | 动作 |
| --- | --- | --- | --- | --- | --- |

### 记忆冲突
| 位置 | 草稿说法 | 记忆记录 | 来源文件 | 解决方式 |
| --- | --- | --- | --- | --- |

### 与上一版的漂移
| 变化类型 | 上一版 | 当前版 | 风险 |
| --- | --- | --- | --- |
```

## LABEL_AUDIT.md

```markdown
# 标注审计

## YYYY-MM-DD - 数据集或标签体系
- 数据集：
- 标签定义版本：
- 对比轮次：
- 完全一致率：
- 人工审查数量：

### 高风险分歧
| 样本 ID | 标签 | 风险原因 | 建议人工动作 |
| --- | --- | --- | --- |

### 标签体系问题
| 标签对 | 症状 | 建议定义调整 |
| --- | --- | --- |
```

## MEMORY_UPDATE_LOG.md

```markdown
# 记忆更新日志

仅用于记录手动、由用户触发的记忆刷新。

## YYYY-MM-DD HH:MM - 手动更新
- 触发方式/来源：
- 已读取文件：
- 已修改文件：
- 已提升事实：
- 仍保留的假设：
- 发现的冲突或过期信息：
- 已建议或已执行的生命周期变更：
- 因不具备长期价值而跳过：
- 下一次建议刷新时点：
```

## RECOVERY_NOTES.md

```markdown
# 恢复记录

## YYYY-MM-DD HH:MM
- 发生了什么变化：
- 当前确定为真：
- 当前阻塞：
- 下一步动作：
- 下次优先读取文件：
```
