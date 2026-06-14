# 来源说明

这个 skill 是一个面向 PM 场景的原创适配版本。它是在阅读若干公开项目记忆和 Agent 连续性项目后形成的，没有打包复制这些项目的源代码、辅助脚本或完整文档。它借鉴的是通用工作流思想，例如基于文件的项目记忆、当前状态摘要、决策日志、交接记录、证据日志和一致性检查。

## 参考项目

| 项目 | 仓库 | 对本 skill 的启发 |
| --- | --- | --- |
| Project Butler | https://github.com/JamesShi96/project-butler | 会话交接、项目档案、更新日志、语言适配、文件模板组织。 |
| RecallLoom | https://github.com/Frappucc1no/recall-loom | 轻量连续性层、快速/深度恢复、当前状态摘要、里程碑证据分离。 |
| project-memory-skill | https://github.com/tasuku-9/project-memory-skill | 规范记忆文件、事实/假设分离、广泛捕捉/谨慎提升、冲突路由。 |
| Memory Bank Skill | https://github.com/fockus/skill-memory-bank | 本地 memory bank 生命周期、与 Agent 无关的结构、确定性辅助脚本思想。 |
| ProjectMem | https://github.com/riponcm/projectmem | 本地优先记忆、类型化项目记录、陈旧度/搜索概念、MCP/CLI 检索思想。 |

## 复用边界

- 没有复制上游项目源代码。
- 没有复制上游完整文档。
- `CURRENT_STATE.md`、`DECISION_LOG.md`、`RECOVERY_NOTES.md` 等文件名被视为通用项目记忆约定。
- 这里对短术语和工作流概念做归因，是为了说明设计来源。

## 发布建议

公开发布这个 skill 前：

1. 如果希望他人复用，请添加你自己的仓库许可证，例如 MIT 或 Apache-2.0。
2. 在公开仓库中保留这个来源说明文件。
3. 如果未来版本复制了上游代码、脚本或大段文本，需要附上对应上游许可证和 notice。
4. 如果未来发布的是包含上游表达的衍生作品，请重新检查每个参考仓库的当前许可证。
