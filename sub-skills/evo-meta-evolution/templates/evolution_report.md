# 🧬 超进化报告

> 自动生成 | Darwin Meta-Evolution

---

## 基本信息

| 属性 | 值 |
|------|-----|
| **目标类型** | `{type}` |
| **扫描路径** | `{path}` |
| **扫描时间** | `{timestamp}` |
| **优化前评分** | `{before_score}/100` |
| **优化后评分** | `{after_score}/100` |
| **提升幅度** | `+{improvement}分` |

---

## 评分详情

### 优化前

| 维度 | 分数 |
|------|------|
| 完整性 | {completeness_before}/100 |
| 一致性 | {consistency_before}/100 |
| 可维护性 | {maintainability_before}/100 |
| 效率 | {efficiency_before}/100 |
| 新鲜度 | {freshness_before}/100 |

### 优化后

| 维度 | 分数 | 变化 |
|------|------|------|
| 完整性 | {completeness_after}/100 | {completeness_change} |
| 一致性 | {consistency_after}/100 | {consistency_change} |
| 可维护性 | {maintainability_after}/100 | {maintainability_change} |
| 效率 | {efficiency_after}/100 | {efficiency_change} |
| 新鲜度 | {freshness_after}/100 | {freshness_change} |

---

## 问题发现

### 🔴 严重问题

{critical_issues}

### 🟡 中等问题

{medium_issues}

### 🟢 轻微问题

{minor_issues}

---

## 优化执行

| 操作 | 文件 | 置信度 | 状态 | 详情 |
|------|------|--------|------|------|
{execution_table}

---

## 未能执行的操作

{pending_actions}

---

## 收益预估

### 效率提升

- **信息检索速度**: {search_speed_improvement}%
- **维护成本**: {maintenance_cost_change}%
- **信息新鲜度**: {freshness_improvement}%

### 质量提升

- **结构清晰度**: +{structure_clarity}分
- **可扩展性**: +{extensibility}分
- **安全性**: +{security}分

---

## 下次可自动优化的点

{auto_optimization_tips}

---

## 详细改动清单

### 新增文件

{new_files}

### 修改文件

{modified_files}

### 删除文件

{deleted_files}

---

## 健康度雷达图

```
        完整性: {completeness_score}
              ↑
              │
  可维护性 ←──┼──→ 一致性
   {maintain_score}       {consistency_score}
              │
              ↓
            效率: {efficiency_score}
              +
            新鲜度: {freshness_score}
```

---

## 建议

### 短期建议（本周内）

{short_term_suggestions}

### 中期建议（本月内）

{medium_term_suggestions}

### 长期建议（季度）

{long_term_suggestions}

---

## 附录

### 分析详情

```json
{analysis_details}
```

### 置信度说明

| 置信度 | 含义 | 行为 |
|--------|------|------|
| ≥ 0.9 | 极高把握 | 直接执行 |
| 0.7-0.9 | 高把握 | 执行，可回滚 |
| 0.5-0.7 | 中等把握 | 先展示方案，确认后执行 |
| < 0.5 | 低把握 | 只提建议，不执行 |

---

_报告生成时间: {report_generated_at}_  
_Darwin Meta-Evolution v1.0.0_
