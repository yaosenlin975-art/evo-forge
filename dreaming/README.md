# 🌙 Darwin Dreaming Core - 梦境记忆整合核心

> 整合自 copaw_dreaming v0.2.x，供 Darwin 技能家族共享使用

---

## 模块结构

```
dreaming/
├── __init__.py                 # 统一导出
├── dreaming_config.py          # 配置模型
├── scoring_engine.py           # 六维评分引擎
├── memory_consolidation.py    # 三阶段睡眠模型
└── README.md                   # 本文件
```

---

## 快速使用

### 方式一：直接导入

```python
from dreaming import (
    ScoringEngine,
    MemoryCandidate,
    run_dreaming,
    DreamingConfig,
)

# 1. 创建配置
config = DreamingConfig()
config.weights.relevance = 0.35  # 自定义权重

# 2. 创建评分引擎
engine = ScoringEngine(config)

# 3. 准备候选记忆
candidates = [
    MemoryCandidate(
        content="用户喜欢简洁的回答",
        source_file="memory/2026-04-12.md",
        keywords=["简洁", "回答"],
    ),
]

# 4. 执行评分
scored = engine.score(candidates)
for item in scored:
    print(f"Score: {item.weighted_score:.2f}, Passed: {item.passed_threshold}")

# 5. 完整记忆整合（三阶段）
report = run_dreaming(
    workspace_dir="/path/to/workspace",
    dry_run=False,
)
```

### 方式二：Agent SOP 模式

在 Agent 执行时，直接按照 SOP 执行：

```
Step 1: 浅睡扫描
- 扫描 memory/ 下所有 .md 文件
- 检查四层目录结构

Step 2: REM 评分
- 运行六维评分引擎
- 应用三重门槛过滤

Step 3: 深睡巩固
- 巩固高分记忆到 L2
- 归档过期记忆到 L4
- 刷新 L1 索引
```

---

## 六维评分信号

| 信号 | 权重 | 说明 |
|------|------|------|
| **relevance** | 0.30 | 与用户核心兴趣的匹配度 |
| **frequency** | 0.24 | 记忆被召回/引用的次数 |
| **query_diversity** | 0.15 | 触发该记忆的不同查询数量 |
| **recency** | 0.15 | 最后更新时间的新鲜度 |
| **consolidation** | 0.10 | 已被引用/关联的程度 |
| **concept_richness** | 0.06 | 包含的概念密度 |

---

## 三重门槛

必须**同时满足**才能进入长期巩固：

```python
config.threshold.min_score = 0.8          # 综合得分 ≥ 0.8
config.threshold.min_recall_count = 3    # 召回次数 ≥ 3
config.threshold.min_unique_queries = 3  # 独立查询数 ≥ 3
```

---

## 四层记忆架构

| 层级 | 文件 | 说明 |
|------|------|------|
| **L1 索引层** | `memory/index.md` | 极简热点指针（≤30行） |
| **L2 事实层** | `MEMORY.md` | 全局事实库 |
| **L3 SOP层** | `memory/sops/` | 任务级 SOP 库 |
| **L4 原始层** | `memory/raw/` | 完整会话存档 |

---

## 配置示例

```python
from dreaming import DreamingConfig

# 默认配置
config = DreamingConfig()

# 自定义配置
config = DreamingConfig(
    threshold_min_score=0.85,
    threshold_min_recall=5,
    threshold_min_unique=4,
)

# 自定义权重
config.weights.relevance = 0.35
config.weights.frequency = 0.20
config.weights.query_diversity = 0.15
config.weights.recency = 0.15
config.weights.consolidation = 0.10
config.weights.concept_richness = 0.05
```

---

## 被谁调用

| 子技能 | 用途 |
|--------|------|
| **darwin-agent-optimizer** | 维度5：记忆进化评分 |
| **darwin-meta-evolution** | 记忆类型优化的核心执行逻辑 |

---

## 版本信息

| 项目 | 版本 |
|------|------|
| Darwin Dreaming Core | v2.0.0 |
| 融合自 | copaw_dreaming v0.2.x |
| 更新日期 | 2026-04-19 |

---

*Darwin Skill 家族 | Dreaming Core 🌙*
