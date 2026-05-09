---
name: evo-forge
description: |
  EvoForge：自主优化器调度器。🧬专家+😈找茬双轨，路由到子技能执行。
  触发词：EvoForge/优化/超进化/审查代码/强化。默认直接执行。
metadata:
  copaw:
    emoji: "🧬"
  skill_version: "13.0.0"
  author: "CoPaw Community"
  changelog: "evo-forge/CHANGELOG.md"
  internal_methods:
    - expert-brainstorm
    - contradiction-analysis
    - nuwa-phase-machine
    - nuwa-dof-control
    - nuwa-parallel-orchestration
    - nuwa-checkpoint
  integrated_knowledge:
    - openclaw_soul: "SOUL配置审查（凌晨两点原则+8条反客服腔+避坑指南）"
    - workflow_orchestration: "Workflow/Activity分离模式"
    - hook_mechanism: "after_complete/on_error/before_start钩子"
    - huashu_nuwa: "女娲Skill创建框架（Phase状态机+多智能体编排+Checkpoint+自由度控制+渐进式披露）"
  sub_skills:
    - evo-agent-optimizer
    - evo-code-review
    - evo-meta-evolution
    - evo-skill-optimizer
    - skill-manager
  parent_skills: []
  merged_from:
    - huashu-nuwa: "多智能体编排/分支控制/Checkpoint/自由度控制/渐进式披露模式"
  source: "customized"
  trigger_words: ['EvoForge', '优化', '超进化', '审查代码', '强化']
---

# EvoForge - 调度器

> **版本**: v13.0.0 | **核心**: 纯调度器，不执行具体优化 ⚡
>
> 📖 CoPaw SOUL | 📡 网络调研 | 🔗 子技能调度 | 🔀 融合集成
>
> **触发词**: EvoForge / 优化 / 超进化 / 审查代码 / 强化

---

## ⚡ 核心原则

> **Workflow/Activity分离**
> - **Workflow（evo-forge）**= 调度逻辑，确定性，不直接执行
> - **Activity（子技能）**= 具体执行，幂等，可重试

**EvoForge只做三件事**：
1. **识别意图**：用户想做什么？
2. **路由到子技能**：哪个子技能负责？
3. **协调结果**：汇总？直接输出？

---

## 🎯 意图识别表

| 用户意图 | 触发词 | 路由到 |
|----------|--------|--------|
| 优化Skill | "优化skill" / "优化xxx" / "强化xxx" | evo-skill-optimizer |
| 优化Agent | "优化agent" / "优化我的" / "强化agent" | evo-agent-optimizer |
| 审查代码 | "审查代码" / "review代码" | evo-code-review |
| 超进化 | "超进化" | evo-meta-evolution |
| 自优化 | "优化EvoForge" / "强化EvoForge" | evo-forge自身(深度=1) |

---

## 🔄 调度流程

```
用户输入 → 意图识别 → 路由到子技能 → 结果处理 → 输出
```

---

## 📡 子技能说明

| 子技能 | 职责 | 核心流程 |
|--------|------|----------|
| **evo-skill-optimizer** | 优化Skill的SKILL.md | Phase 0→0.5→0.7→1→2→3 |
| **evo-agent-optimizer** | 优化Agent核心文件 | Phase 0→1→2→3 |
| **evo-code-review** | 审查代码质量 | Phase 0→1→2→3 |
| **evo-meta-evolution** | 元进化（配置/文档/知识优化） | 步骤1→2→3→4→5 |

---

## 🔀 融合集成（使用skill-manager.skill-merger）

> 调研发现优秀模式需要融入时，使用skill-merger执行融合。

**融合触发条件**：
- 调研模式与现有技能功能重叠 ≥ 40%
- 用户明确要求融合
- 功能互补且总触发词 ≤ 3 个

**融合调用**：
```python
chat_with_agent(
    to_agent="skill-manager",
    text="融合 [技能A] 和 [技能B]"
)
```

---

## 🌀 Phase 状态机（女娲融合）

> 源：huashu-nuwa 多智能体编排框架 | 适用：多Phase复杂工作流的分支控制+状态追踪

当路由到子技能后发现它支持多Phase工作流且有条件分支路径时，启用Phase状态机：

```
用户输入 → Phase 0（入口分流）→ switch-case → Phase 1（数据采集）
                                                      ↓
                                            Phase 2（深度推理/高自由度）
                                                      ↓
                                            Phase 3-5（验证/增强）
                                                      ↓
                                            Checkpoint → 用户确认 → 输出
```

### 分支规则

| Phase | 类型 | 自由度 | 说明 |
|-------|------|--------|------|
| Phase 0 | 入口分类 | 低 | switch-case 根据输入分流，不走回头路 |
| Phase 0.5 | 初始化 | 低 | 目录/脚本/环境准备，确定性执行 |
| Phase 1 | 数据采集 | 低 | 并行或顺序获取原始数据 |
| Phase 2 | 深度推理 | **高** | 允许AI进行受控的心智建模，非简单摘要 |
| Phase 3-5 | 验证/打包 | 低→中 | 检查点+修复+输出 |

### Phase 0 入口分流模式

```python
match input_type:
    case "优化Skill":       → evo-skill-optimizer (全Phase)
    case "优化Agent":      → evo-agent-optimizer (全Phase)
    case "审查代码":       → evo-code-review (Phase 0→1→2→3)
    case "超进化":         → evo-meta-evolution (步骤1→2→3→4→5)
    case "自优化":         → evo-forge自身 (深度=1)
```

### 状态追踪

每个 Phase 执行后记录状态，支持中断恢复：

- `state/phase.md`：记录当前执行到哪个Phase、已完成/失败/暂停
- `state/outputs/`：每个Phase产出的中间结果
- 中断后下次调用从最近的 Checkpoint 继续

---

## 🎯 自由度控制（DF Control — 女娲融合）

> 源：huashu-nuwa Degrees of Freedom 精准受控 | 适用：区分自动化执行 vs 深度推理路径

| 自由度 | 适用Phase | 行为特征 | 实例 |
|--------|-----------|----------|------|
| **低 DF** | 初始化/数据采集/验证/打包 | 脚本驱动+固定目录，确定性输出 | Phase 0.5 创建目录结构、Phase 1 抓取数据 |
| **高 DF** | 深度提炼/心智建模/策略生成 | AI自由推理但受框架约束 | Phase 2 提炼核心洞察、策略推荐 |

**决策规则**：
- 输出格式/命名/路径 → **低DF**，硬编码在Phase流程中，不走样
- 内容生成/策略建议/优化方向 → **高DF**，允许创造性但受方法论框架约束（如找茬循环、矛盾分析）
- 同一子技能混合使用两种DF：自动化步骤走低DF，推理步骤走高DF

---

## 🔁 并行多Agent编排（女娲融合）

> 源：huashu-nuwa 主控Agent → 6个子Agent并行采集 | 适用：独立子任务并行执行

当任务可拆分为多个**无依赖**的子任务时，启用并行编排模式：

### 流程

```
主控Agent拆解任务
   ↓
识别无依赖子任务 → 并行分派到多个子Agent/子技能
   ↓ (每个独立写入自己的输出文件)
每个子Agent完成 → 主控汇总
   ↓
主控交叉验证一致性
   ↓
输出最终结果
```

### 并行触发条件

- [x] 子任务之间无数据依赖
- [x] 每个子任务有明确的独立输出边界
- [x] 主控有能力做一致性校验

### 串联回退条件

- [ ] 子任务有顺序依赖
- [ ] 输出需要全局上下文
- [ ] 需要共享状态 → 回退到串联执行

---

## ⏸️ Checkpoint 硬暂停（女娲融合）

> 源：huashu-nuwa 闭环质检与自愈 | 适用：不可逆操作/关键决策点前的用户确认

### 硬性检查点规则

| 检查点类型 | 触发条件 | 行为 |
|-----------|----------|------|
| CP1 | Phase 完成、即将执行不可逆操作 | **暂停**，问用户确认 |
| CP2 | 输出结果待发布/对外发送 | **暂停**，展示结果摘要给用户 |
| CP3 | 检测到死循环/迭代超限 | **强制终止**，返回失败报告 |

### 暂停协议

```
EvoForge: [CP1] Phase 1 数据采集完成，共获取 N 条数据。
          ⚠️ 即将进入 Phase 2 深度推理阶段，该阶段不可逆。
          确认继续？(y/n)
用户: y
EvoForge: → 继续 Phase 2
```

### 迭代上限保护

| 场景 | 上限 | 超限处理 |
|------|------|----------|
| 找茬循环 | 5轮 | 强制终止，输出已解决的问题列表 |
| Phase 重试 | 3次 | 标记失败，回滚到上一个Checkpoint |
| 并行Agent等待 | 120秒 | 超时的Agent标记为失败，继续汇总 |

---

## 🌀 找茬循环

**终止**：连续2轮无茬 | **最大**：5轮

| # | 问题 | 检查点 |
|---|------|--------|
| 1 | 路由对吗？ | 意图识别正确？子技能匹配？ |
| 2 | 用户会骂吗？ | 路由错误？找不到子技能？ |
| 3 | 子技能一致吗？ | 有sub_skills列表但不调用？ |

---

## ⚖️ 矛盾分析

**触发**：trade-off、瓶颈、多问题
```
Step 1: 列出矛盾
Step 2: 识别主要矛盾
Step 3: 分析性质
Step 4: 确定方案
```

---

## 🔴 红线标准

| 检查项 | 红线 | 判断 |
|--------|------|------|
| 子技能列表删除 | >0 | 任何删除sub_skills字段 |
| 路由表删除 | >0 | 任何删除意图识别表 |
| 触发词减少 | >50% | 超过一半 |

**触发红线 → 禁止优化**

---

## 🛡️ 护栏检查

| 护栏 | 检查点 |
|------|--------|
| **路由完整性** | 所有子技能都有路由？ |
| **向后兼容** | 现有用户能继续使用？ |
| **大小限制** | ≤250行为宜 |

**触发护栏失败 → 需用户确认**

---

## 📋 优化报告格式

```markdown
## 🧬 调度报告

### 意图识别
| 项目 | 值 |
|------|-----|
| 用户输入 | xxx |
| 识别意图 | 优化Skill |
| 路由到 | evo-skill-optimizer |

### 执行结果
| 项目 | 值 |
|------|-----|
| 子技能 | evo-skill-optimizer |
| 执行状态 | ✅完成 |
| 优化评分 | 95/100 |
```

---

---

## 📋 优化日志规范

### 日志存储位置
所有优化报告和日志必须写入**被优化目标**的 `evo-forge/` 文件夹，而非根目录或 SKILL.md frontmatter 中：

| 场景 | 旧位置（废弃） | 新位置 |
|------|---------------|--------|
| Skill 优化报告 | `{skill}/OPTIMIZATION_REPORT.md` 或 SKILL.md frontmatter | `{skill}/evo-forge/OPTIMIZATION_REPORT.md` |
| Agent 优化报告 | `{agent}/OPTIMIZATION_REPORT.md` 或 SOUL.md frontmatter | `{agent}/evo-forge/OPTIMIZATION_REPORT.md` |
| 版本变更记录 | `{skill}/CHANGELOG.md` | `{skill}/evo-forge/CHANGELOG.md` |
| 整合报告 | `{skill}/INTEGRATION_REPORT.md` | `{skill}/evo-forge/INTEGRATION_REPORT.md` |

### EvoForge 自身日志
EvoForge 自身的日志存放在 `skills/evo-forge/evo-forge/` 目录下：
- `skills/evo-forge/evo-forge/CHANGELOG.md` — 版本历史
- `skills/evo-forge/evo-forge/INTEGRATION_REPORT.md` — 整合报告

### 操作原则
1. **禁止**往目标的 SKILL.md/SOUL.md 等文件的 frontmatter 写 `update_log` 字段
2. 优化报告统一写入 `{target}/evo-forge/` 目录下的独立文件
3. 每次优化前检查该目录是否存在，不存在则创建

---

## 💡 实战示例

### 示例1: 批量优化所有custom技能
```
用户: "优化所有custom技能"
EvoForge:
  1. 识别意图 → 优化Skill → 路由到 evo-skill-optimizer
  2. 调用子技能执行批量优化
  3. 返回优化报告
```

### 示例2: 自优化（递归控制=1）
```
用户: "优化EvoForge" / "EvoForge优化EvoForge"
EvoForge:
  1. 识别为自优化请求
  2. 设置递归深度=1
  3. 对 evo-forge/SKILL.md 执行优化
  4. 由当前Agent执行（非自身递归）
```

### 示例3: 网络调研+融合
```
用户: "优化skill-manager，调研最佳实践后融合"
EvoForge:
  1. 执行Phase 3.5网络调研（skills.sh等）
  2. 评估是否需要融合
  3. 调用 skill-manager.skill-merger 执行融合
  4. 返回融合报告
```

### 示例4: 代码审查
```
用户: "帮我审查 /app/working/workspaces/default 下的代码"
EvoForge:
  1. 识别意图 → 审查代码 → 路由到 evo-code-review
  2. 调用子技能执行代码审查
  3. 返回审查报告
```

### 示例5: Agent优化
```
用户: "优化我的Agent"
EvoForge:
  1. 识别意图 → 优化Agent → 路由到 evo-agent-optimizer
```
