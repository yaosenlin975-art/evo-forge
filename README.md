<div align="center">
  <a href="#section-zh"><img src="https://img.shields.io/badge/🇨🇳-中文-blue?style=for-the-badge" alt="中文"></a>
  &nbsp;&nbsp;
  <a href="#section-en"><img src="https://img.shields.io/badge/🇬🇧-English-blue?style=for-the-badge" alt="English"></a>
</div>

---

<h1 align="center">EvoForge</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-13.0.0-brightgreen" alt="Version 13.0.0">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License">
</p>

> **致敬 [Drawin](https://github.com/alchaincyf)** — EvoForge 的原始架构与核心循环设计深受 Drawin 的 [autoresearch](https://github.com/karpathy/autoresearch) 启发。将自主实验循环从模型训练搬到 Skill 优化领域，一个只能向前转的棘轮。致敬原始创作者的思想与贡献。

---

---

## <a id="section-zh"></a>🇨🇳 中文说明

### 简介

EvoForge：自主优化器调度器。

### 文件结构

```
evo-forge/
├── README.md
├── showcase.html
├── SKILL.md
```

### 安装

将 `evo-forge` 目录放入工作区的 `skills/` 目录下即可使用。

### 使用方式

详细用法请参考 `SKILL.md`。

### 依赖

- QwenPaw / CoPaw 环境
- Python 3.8+

### 子技能

| 子技能 | 说明 |
|--------|------|
| `evo-agent-optimizer` | Agent 优化器 - 优化 Agent 的核心文件（SOUL.md/SKILL.md/PROFILE.md）。 |
| `evo-code-review` | 代码审查器 - 代码质量审查。 |
| `evo-meta-evolution` | Meta Evolution - 🧬专家视角整合跨Agent知识 + 😈找茬视角审查内容质量。 |
| `evo-skill-optimizer` | Skill 优化器 - 优化技能的 SKILL.md。 |


---

## <a id="section-en"></a>🇬🇧 English Documentation

### Introduction

EvoForge：自主优化器调度器。🧬专家+😈找茬双轨，路由到子技能执行

### 文件结构

```
evo-forge/
├── README.md
├── showcase.html
├── SKILL.md
```

### 安装

Place the `evo-forge` directory into the `skills/` directory of your workspace.

### 使用方式

Refer to `SKILL.md` for detailed usage.

### 依赖

- QwenPaw / CoPaw environment
- Python 3.8+

### Sub-skills

| 子技能 | 说明 |
|--------|------|
| `evo-agent-optimizer` | Agent 优化器 - 优化 Agent 的核心文件（SOUL.md/SKILL.md/PROFILE.md）。 双视角审查，SOUL配置健康度评估 |
| `evo-code-review` | 代码审查器 - 代码质量审查。双视角审查（🧬专家+😈找茬），圈复杂度/重复度/安全性检查，支持多语言 |
| `evo-meta-evolution` | Meta Evolution - 🧬专家视角整合跨Agent知识 + 😈找茬视角审查内容质量。将多个Agent知识提炼为全局信息，知识无效=没整合。v7.0双视角融合。 |
| `evo-skill-optimizer` | Skill 优化器 - 优化技能的 SKILL.md。双视角审查（🧬专家+😈找茬）， 8维度评分+1依赖维度，维护+增强+拆分+依赖修复四重优化 |

