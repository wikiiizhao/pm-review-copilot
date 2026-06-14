#!/usr/bin/env python3
"""创建中文 PM 审查记忆工作区。"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


TEMPLATES: dict[str, str] = {
    "CONTEXT_MANIFEST.md": """# 上下文清单

## 项目
- 名称：{project_name}
- 负责人：
- 记忆目录：`{memory_root}/`
- 文档语言：中文

## 读取顺序
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

## 规范职责
- 用户风格和审查偏好：`USER_PREFERENCES.md`
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

## 忽略
- `.git/`
- `node_modules/`
- `dist/`
- `build/`
- `.cache/`
- `tmp/`
- 生成导出物，除非用户明确要求
""",
    "USER_PREFERENCES.md": """# 用户偏好

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
""",
    "CURRENT_STATE.md": """# 当前状态

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
""",
    "DECISION_LOG.md": """# 决策日志

## YYYY-MM-DD - 决策标题
- 状态：已采纳 | 已拒绝 | 延后 | 已被替代
- 背景：
- 考虑过的选项：
- 决策：
- 理由：
- 风险：
- 复盘条件：
- 证据链接：
""",
    "EVIDENCE_LOG.md": """# 证据日志

## YYYY-MM-DD - 证据标题
- 来源：
- 方法：
- 发现：
- 置信度：低 | 中 | 高
- 限制：
- 影响：
- 相关假设：
""",
    "HYPOTHESIS_LAB.md": """# 假设实验室

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
""",
    "HUMAN_BRIEF.md": """# 人类简报

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
""",
    "REVIEW_LOG.md": """# 审查日志

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
""",
    "LABEL_AUDIT.md": """# 标注审计

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
""",
    "MEMORY_UPDATE_LOG.md": """# 记忆更新日志

仅用于记录手动、由用户触发的记忆刷新。

## YYYY-MM-DD HH:MM - 手动更新
- 触发方式/来源：
- 已读取文件：
- 已修改文件：
- 已提升事实：
- 仍保留的假设：
- 发现的冲突或过期信息：
- 因不具备长期价值而跳过：
- 下一次建议刷新时点：
""",
    "RECOVERY_NOTES.md": """# 恢复记录

## {timestamp}
- 发生了什么变化：PM 记忆工作区已初始化。
- 当前确定为真：
- 当前阻塞：
- 下一步动作：
- 下次优先读取文件：`CONTEXT_MANIFEST.md`、`HUMAN_BRIEF.md`、`USER_PREFERENCES.md`、`CURRENT_STATE.md`
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
    parser = argparse.ArgumentParser(description="创建中文 PM 审查记忆文件。")
    parser.add_argument("--path", default=".", help="项目或工作区路径。")
    parser.add_argument("--memory-root", default="pm-memory", help="记忆文件夹名称。")
    parser.add_argument("--project-name", default="未命名 PM 项目")
    parser.add_argument("--force", action="store_true", help="覆盖已有文件。")
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

    print(f"记忆目录：{memory}")
    print(f"已创建：{len(created)}")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print(f"已跳过的现有文件：{len(skipped)}")
        for item in skipped:
            print(f"  = {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
