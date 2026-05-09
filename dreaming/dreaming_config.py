"""
copaw-dreaming v0.2.0 - 配置模型与默认值

v0.2.0 新增：
- 四层记忆架构配置 (L1-L4)
- Gene/Capsule 进化机制配置
- 安全配置 (rollback, dry-run, human review)
- Evolution Events 流配置

使用 dataclass + 验证，支持 Skill 模式和 Plugin 模式。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class SleepPhase(str, Enum):
    """睡眠阶段枚举"""
    PREPARATION = "preparation"
    LIGHT_SLEEP = "light_sleep"
    REM_SLEEP = "rem_sleep"
    DEEP_SLEEP = "deep_sleep"


class GeneCategory(str, Enum):
    """基因类别枚举（借鉴 EvoMap GEP）"""
    REPAIR = "repair"           # 修复型：处理错误/异常/失败
    OPTIMIZE = "optimize"       # 优化型：性能/协议/提示优化
    CONSOLIDATE = "consolidate" # 巩固型：高分记忆沉淀
    CLEANUP = "cleanup"         # 清理型：过期/低价值记忆处理


class MemoryLayer(str, Enum):
    """记忆层级枚举（借鉴 GenericAgent L1-L4）"""
    L1_INDEX = "l1_index"    # 索引层：极简热点指针
    L2_FACTS = "l2_facts"    # 事实层：全局事实库
    L3_SOPS = "l3_sops"      # SOP层：任务级SOP库
    L4_RAW = "l4_raw"        # 原始层：完整会话存档


@dataclass
class WeightsConfig:
    """六信号权重配置"""
    relevance: float = 0.30
    frequency: float = 0.24
    query_diversity: float = 0.15
    recency: float = 0.15
    consolidation: float = 0.10
    concept_richness: float = 0.06

    def __post_init__(self):
        total = sum([
            self.relevance, self.frequency, self.query_diversity,
            self.recency, self.consolidation, self.concept_richness
        ])
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Weights must sum to 1.0, got {total:.4f}")

    def as_dict(self) -> Dict[str, float]:
        return {
            "relevance": self.relevance,
            "frequency": self.frequency,
            "query_diversity": self.query_diversity,
            "recency": self.recency,
            "consolidation": self.consolidation,
            "concept_richness": self.concept_richness,
        }


@dataclass
class ThresholdConfig:
    """三重门槛配置"""
    min_score: float = 0.8           # 最低综合得分
    min_recall_count: int = 3        # 最少召回次数
    min_unique_queries: int = 3      # 最少独立查询数

    def check(self, score: float, recall: int, unique: int) -> bool:
        """检查是否通过所有门槛"""
        return (
            score >= self.min_score and
            recall >= self.min_recall_count and
            unique >= self.min_unique_queries
        )


# ============================================================
# v0.2.0 新增：四层记忆架构配置
# ============================================================

@dataclass
class MemoryLayerConfig:
    """单个记忆层配置"""
    enabled: bool = True
    max_entries: int = 50          # 最大条目数
    auto_update: bool = True       # 是否自动更新


@dataclass
class MemoryLayersConfig:
    """四层记忆架构配置（借鉴 GenericAgent L1-L4）"""
    l1_index: MemoryLayerConfig = field(default_factory=lambda: MemoryLayerConfig(
        enabled=True,
        max_entries=30,      # L1 保持极简
        auto_update=True,
    ))
    l2_facts: MemoryLayerConfig = field(default_factory=lambda: MemoryLayerConfig(
        enabled=True,
        max_entries=100,
        auto_update=True,
    ))
    l3_sops: MemoryLayerConfig = field(default_factory=lambda: MemoryLayerConfig(
        enabled=True,
        max_entries=50,
        auto_update=True,
    ))
    l4_raw: MemoryLayerConfig = field(default_factory=lambda: MemoryLayerConfig(
        enabled=True,
        max_entries=1000,    # L4 可以较多
        auto_update=True,
    ))

    def get_layer_path(self, layer: MemoryLayer) -> str:
        """获取指定层的默认路径"""
        paths = {
            MemoryLayer.L1_INDEX: "memory/index.md",
            MemoryLayer.L2_FACTS: "MEMORY.md",
            MemoryLayer.L3_SOPS: "memory/sops",
            MemoryLayer.L4_RAW: "memory/raw",
        }
        return paths.get(layer, "")


# ============================================================
# v0.2.0 新增：Gene/Capsule 进化机制配置
# ============================================================

@dataclass
class GeneMatchConditions:
    """Gene 匹配条件"""
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    category: Optional[str] = None
    memory_type: Optional[str] = None
    source_file_pattern: Optional[str] = None
    recall_count_min: Optional[int] = None

    def matches(self, score: float = 0, recall: int = 0, category: str = "", **kwargs) -> bool:
        """检查是否匹配条件"""
        if self.min_score is not None and score < self.min_score:
            return False
        if self.max_score is not None and score > self.max_score:
            return False
        if self.category is not None and category != self.category:
            return False
        if self.recall_count_min is not None and recall < self.recall_count_min:
            return False
        return True


@dataclass
class Gene:
    """基因定义（借鉴 EvoMap GEP Gene）"""
    id: str
    category: GeneCategory
    description: str
    match_conditions: GeneMatchConditions
    strategy: str = ""
    priority: int = 10
    enabled: bool = True
    triggered_count: int = 0
    success_count: int = 0

    @property
    def success_rate(self) -> float:
        if self.triggered_count == 0:
            return 0.0
        return self.success_count / self.triggered_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category.value if isinstance(self.category, GeneCategory) else self.category,
            "description": self.description,
            "match_conditions": asdict(self.match_conditions),
            "strategy": self.strategy,
            "priority": self.priority,
            "enabled": self.enabled,
            "triggered_count": self.triggered_count,
            "success_count": self.success_count,
            "success_rate": round(self.success_rate, 3),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Gene":
        conditions = GeneMatchConditions(**data.get("match_conditions", {}))
        return cls(
            id=data["id"],
            category=GeneCategory(data["category"]) if isinstance(data["category"], str) else data["category"],
            description=data.get("description", ""),
            match_conditions=conditions,
            strategy=data.get("strategy", ""),
            priority=data.get("priority", 10),
            enabled=data.get("enabled", True),
            triggered_count=data.get("triggered_count", 0),
            success_count=data.get("success_count", 0),
        )


@dataclass
class Capsule:
    """胶囊定义（借鉴 EvoMap GEP Capsule）"""
    id: str
    trigger_conditions: Dict[str, Any]
    outcome: str
    validated_count: int = 0
    failed_count: int = 0
    first_validated_at: Optional[str] = None
    last_validated_at: Optional[str] = None
    memory_ids: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        total = self.validated_count + self.failed_count
        if total == 0:
            return 0.0
        return self.validated_count / total

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "trigger_conditions": self.trigger_conditions,
            "outcome": self.outcome,
            "validated_count": self.validated_count,
            "failed_count": self.failed_count,
            "success_rate": round(self.success_rate, 3),
            "first_validated_at": self.first_validated_at,
            "last_validated_at": self.last_validated_at,
            "memory_ids": self.memory_ids,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Capsule":
        return cls(
            id=data["id"],
            trigger_conditions=data.get("trigger_conditions", {}),
            outcome=data.get("outcome", ""),
            validated_count=data.get("validated_count", 0),
            failed_count=data.get("failed_count", 0),
            first_validated_at=data.get("first_validated_at"),
            last_validated_at=data.get("last_validated_at"),
            memory_ids=data.get("memory_ids", []),
        )


@dataclass
class GeneSystemConfig:
    """Gene/Capsule 系统配置"""
    genes_file: str = "memory/genes.json"
    capsules_file: str = "memory/capsules.json"
    events_file: str = "memory/events.jsonl"
    min_validation_count: int = 3  # 验证成功次数才能成为胶囊
    capsule_success_threshold: float = 0.9  # 胶囊验证成功率阈值
    gene_learning_enabled: bool = True  # 是否自动学习新基因


@dataclass
class SafetyConfig:
    """安全机制配置（借鉴 EvoMap GEP 安全机制）"""
    rollback_enabled: bool = True        # 是否启用回滚
    dry_run_default: bool = False        # 默认 dry-run 模式
    human_review_threshold: int = 5      # 超过此数量操作需人工确认
    backup_retention_days: int = 30      # 备份保留天数
    backup_dir: str = "memory/backups"
    require_review_for_deletions: bool = True  # 删除操作是否需要审查
    max_auto_archive_per_run: int = 20   # 每次最多自动归档数量


@dataclass
class LightSleepConfig:
    """浅睡阶段配置"""
    max_memory_age_days: int = 30          # 只处理 N 天内的记忆
    scan_batch_size: int = 50              # 每批扫描数量
    min_paragraph_length: int = 10         # 最小段落长度（字符）
    exclude_patterns: List[str] = field(default_factory=lambda: [
        r"^## .*",           # 标题行
        r"^---",             # 分隔线
        r"^\s*$",           # 空行
        r"^\|",             # 表格行
        r"^- \[x\]",       # 已完成 todo（纯操作记录）
    ])


@dataclass
class REMSleepConfig:
    """REM睡眠阶段配置"""
    max_candidates: int = 20               # REM 阶段最多处理候选数
    association_depth: int = 2             # 联想深度（跳数）
    min_insight_score: float = 0.6         # 生成洞察的最低关联分
    cross_topic_threshold: float = 0.4     # 跨主题连接阈值


@dataclass
class DeepSleepConfig:
    """深睡阶段配置"""
    archive_threshold_days: int = 90       # 超过此天数的记忆归档
    max_consolidations_per_run: int = 10  # 每次最多巩固条目数
    keep_recent_versions: int = 3         # 保留最近几个版本
    archive_compress: bool = True          # 是否压缩归档文件
    create_sop_threshold: int = 3          # 同一任务成功次数达到此值时创建 SOP


@dataclass
class ScheduleConfig:
    """调度配置"""
    cron_expression: str = "0 2 * * *"     # 默认每天凌晨2点
    timezone: str = "Asia/Shanghai"
    enabled: bool = True


@dataclass
class DreamingConfig:
    """完整梦境配置"""
    # 核心配置
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)
    weights: WeightsConfig = field(default_factory=WeightsConfig)
    
    # v0.2.0 新增：四层记忆架构
    memory_layers: MemoryLayersConfig = field(default_factory=MemoryLayersConfig)
    
    # v0.2.0 新增：Gene/Capsule 系统
    gene_system: GeneSystemConfig = field(default_factory=GeneSystemConfig)
    
    # v0.2.0 新增：安全机制
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    
    # 阶段配置
    light_sleep: LightSleepConfig = field(default_factory=LightSleepConfig)
    rem_sleep: REMSleepConfig = field(default_factory=REMSleepConfig)
    deep_sleep: DeepSleepConfig = field(default_factory=DeepSleepConfig)
    
    # 调度配置
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    
    # 路径配置
    memory_dir: str = "memory"
    long_term_file: str = "MEMORY.md"
    archive_dir: str = "memory/archive"
    state_file: str = "memory/.dreaming_state.json"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            "thresholds": asdict(self.thresholds),
            "weights": self.weights.as_dict(),
            "memory_layers": {
                "l1_index": asdict(self.memory_layers.l1_index),
                "l2_facts": asdict(self.memory_layers.l2_facts),
                "l3_sops": asdict(self.memory_layers.l3_sops),
                "l4_raw": asdict(self.memory_layers.l4_raw),
            },
            "gene_system": asdict(self.gene_system),
            "safety": asdict(self.safety),
            "light_sleep": asdict(self.light_sleep),
            "rem_sleep": asdict(self.rem_sleep),
            "deep_sleep": asdict(self.deep_sleep),
            "schedule": asdict(self.schedule),
            "paths": {
                "memory_dir": self.memory_dir,
                "long_term_file": self.long_term_file,
                "archive_dir": self.archive_dir,
                "state_file": self.state_file,
            },
        }


# ============================================================
# 默认配置实例
# ============================================================

DEFAULT_CONFIG = DreamingConfig()


# ============================================================
# 内置默认基因工厂
# ============================================================

class DefaultGenes:
    """内置默认基因工厂（借鉴 EvoMap GEP Gene 定义）"""
    
    @staticmethod
    def create_default_genes() -> List[Gene]:
        """创建默认基因列表"""
        return [
            Gene(
                id="gene_consolidate_high_value",
                category=GeneCategory.CONSOLIDATE,
                description="巩固高分记忆（评分>=0.8, 召回>=3）",
                match_conditions=GeneMatchConditions(
                    min_score=0.8,
                    recall_count_min=3,
                ),
                strategy="将记忆写入 MEMORY.md，更新索引层",
                priority=5,
                enabled=True,
            ),
            Gene(
                id="gene_cleanup_stale",
                category=GeneCategory.CLEANUP,
                description="归档过期记忆（超过90天无召回）",
                match_conditions=GeneMatchConditions(),
                strategy="移动到 archive/ 目录，保留指针",
                priority=8,
                enabled=True,
            ),
            Gene(
                id="gene_sop_extract",
                category=GeneCategory.OPTIMIZE,
                description="提取成功任务为 SOP（同一任务成功>=3次）",
                match_conditions=GeneMatchConditions(
                    category="optimize",
                ),
                strategy="生成 sops/{task_type}_sop.md",
                priority=7,
                enabled=True,
            ),
            Gene(
                id="gene_repair_missing",
                category=GeneCategory.REPAIR,
                description="修复缺失的索引引用",
                match_conditions=GeneMatchConditions(
                    category="repair",
                ),
                strategy="重建索引，更新引用关系",
                priority=3,  # 修复型优先级较高
                enabled=True,
            ),
            Gene(
                id="gene_index_refresh",
                category=GeneCategory.OPTIMIZE,
                description="刷新 L1 索引层热点指针",
                match_conditions=GeneMatchConditions(),
                strategy="更新 index.md 中的热点记忆指针",
                priority=9,
                enabled=True,
            ),
            Gene(
                id="gene_layer_upgrade",
                category=GeneCategory.CONSOLIDATE,
                description="将 L4 原始记忆升级到更高层",
                match_conditions=GeneMatchConditions(
                    recall_count_min=2,
                ),
                strategy="评估并提升记忆到 L3 SOP 或 L2 事实层",
                priority=6,
                enabled=True,
            ),
        ]

    @staticmethod
    def get_default_genes_data() -> List[Dict[str, Any]]:
        """获取默认基因数据（用于序列化）"""
        return [gene.to_dict() for gene in DefaultGenes.create_default_genes()]

   