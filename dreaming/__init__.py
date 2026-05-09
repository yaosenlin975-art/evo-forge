"""
Darwin Skill - Dreaming Core (梦境核心)
=========================================

本模块整合了 copaw_dreaming 的核心功能，供 Darwin 技能家族使用。

核心模块：
- dreaming_config.py: 配置模型 + 六维评分权重 + 三重门槛
- scoring_engine.py: 六信号评分引擎
- memory_consolidation.py: 三阶段睡眠模型

使用示例：
    from dreaming import ScoringEngine, MemoryCandidate, run_dreaming
    
    # 快速评分
    engine = ScoringEngine()
    candidates = [MemoryCandidate(content="...", source_file="test.md")]
    scored = engine.score(candidates)
    
    # 完整记忆整合
    report = run_dreaming(workspace_dir="/path/to/workspace", dry_run=False)

版本: v2.0.0
融合: copaw_dreaming v0.2.x
"""

from .scoring_engine import ScoringEngine, MemoryCandidate, MemorySignals
from .dreaming_config import (
    DreamingConfig,
    WeightsConfig,
    ThresholdConfig,
    SleepPhase,
    MemoryLayer,
)
from .memory_consolidation import run_dreaming, get_evolution_status

__all__ = [
    # 核心类
    "ScoringEngine",
    "MemoryCandidate",
    "MemorySignals",
    "DreamingConfig",
    "WeightsConfig",
    "ThresholdConfig",
    # 枚举
    "SleepPhase",
    "MemoryLayer",
    # 函数
    "run_dreaming",
    "get_evolution_status",
]

__version__ = "2.0.0"
