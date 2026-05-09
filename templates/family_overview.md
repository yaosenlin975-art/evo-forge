# EvoForge 技能家族总览

> EvoForge 是一系列优化工具的集合，帮助你提升 CoPaw 系统中的 Skills、Agents 和代码质量。

## 家族成员

| 技能 | 职责 | 触发词 |
|------|------|--------|
| **evo-forge** | 协调器（入口） | "EvoForge"、"优化" |
| **evo-skill-optimizer** | Skill 优化 | "优化 skill" |
| **evo-agent-optimizer** | Agent 优化 | "优化 agent" |
| **evo-code-review** | 代码审查 | "审查代码" |

## 共享资源

```
/app/working/skill_pool/evo-forge/
├── rubrics/              # 评估标准库
│   ├── skill_rubric.md
│   └── code_review_rubric.md
├── results/              # 优化记录
│   ├── skill_results.tsv
│   ├── agent_results.tsv
│   └── code_review_results.tsv
└── templates/            # 输出模板
    └── family_overview.md
```

## 快速开始

```bash
# 优化一个 Skill
"优化 skill" / "优化 xxx 技能"

# 优化一个 Agent
"优化 agent" / "优化我的 default agent"

# 审查代码
"审查代码" / "review 这段 Python"
```

## 设计理念

1. **单一职责** - 每个子技能只做一件事
2. **共享资源** - rubric 和结果统一管理
3. **独立演进** - 子技能可以独立优化升级
4. **协同工作** - 优化 Skill/Agent 时可自动触发代码审查

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.1 | 2026-05-07 | 重命名 god-hand → evo-forge，达尔文 → EvoForge |
| v2.0 | 2026-04-17 | 从单一文件拆分为4个子技能 |
| v1.x | 2026-04-15 | 初始版本，包含3种模式 |
