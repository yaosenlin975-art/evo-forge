#!/usr/bin/env python3
"""
记忆整合脚本 - copaw-dreaming v0.2.0

执行三阶段记忆整合流程：浅睡 → REM → 深睡
支持四层记忆架构、Gene/Capsule 进化机制、Rollback 安全机制

使用方法:
    python -m skills.copaw_dreaming.scripts.memory_consolidation --workspace /path/to/workspace
    python -m skills.copaw_dreaming.scripts.memory_consolidation --workspace /path/to/workspace --dry-run
    python -m skills.copaw_dreaming.scripts.memory_consolidation --workspace /path/to/workspace --status
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# 导入新模块
from .dreaming_daemon import DreamingDaemon, get_evolution_status, run_dreaming
from .dreaming_config import DEFAULT_CONFIG, DreamingConfig


def main():
    parser = argparse.ArgumentParser(
        description="copaw-dreaming v0.2.0 - 梦境记忆整合系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --workspace /path/to/workspace              # 执行一次记忆整合
  %(prog)s --workspace /path/to/workspace --dry-run    # 模拟运行
  %(prog)s --workspace /path/to/workspace --status     # 查看进化状态

借鉴设计:
  - GenericAgent L1-L4 Memory Architecture
  - EvoMap GEP (Genome Evolution Protocol)
        """,
    )

    parser.add_argument(
        "--workspace",
        type=str,
        default=".",
        help="工作区目录路径 (默认: 当前目录)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模拟运行模式，不实际写入任何文件",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="查看 Gene/Capsule 进化状态",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="自定义配置文件路径 (JSON)",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        help="设置最低评分门槛 (覆盖配置)",
    )
    parser.add_argument(
        "--report-format",
        choices=["json", "markdown", "simple"],
        default="simple",
        help="报告输出格式",
    )

    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()

    # 加载自定义配置
    config = None
    if args.config:
        config_path = Path(args.config)
        if config_path.exists():
            config_data = json.loads(config_path.read_text(encoding="utf-8"))
            config = _dict_to_config(config_data)
            print(f"📋 加载自定义配置: {config_path}")
        else:
            print(f"⚠️ 配置文件不存在: {config_path}, 使用默认配置")

    # 如果指定了 min-score，更新配置
    if args.min_score is not None:
        if config is None:
            config = DEFAULT_CONFIG
        config.thresholds.min_score = args.min_score
        print(f"📋 覆盖最低评分门槛: {args.min_score}")

    # 查看状态模式
    if args.status:
        _print_evolution_status(workspace)
        return 0

    # 执行记忆整合
    print("🌙" + "=" * 50)
    print("  copaw-dreaming v0.2.0")
    print("  四层记忆架构 + Gene/Capsule 进化")
    print("=" * 53)
    print(f"📁 工作区: {workspace}")
    print(f"🔍 运行模式: {'Dry-Run (模拟)' if args.dry_run else 'Live (实际执行)'}")
    print()

    try:
        daemon = DreamingDaemon(
            workspace_dir=workspace,
            config=config,
            dry_run=args.dry_run,
        )

        report = daemon.run_once()

        # 输出报告
        if args.report_format == "json":
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            _print_report(report, args.report_format)

        # 返回状态码
        return 0 if report["status"] == "completed" else 1

    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def _dict_to_config(data: dict) -> DreamingConfig:
    """将字典转换为配置对象（简化实现）"""
    config = DreamingConfig()

    # 更新 thresholds
    if "thresholds" in data:
        for key, value in data["thresholds"].items():
            if hasattr(config.thresholds, key):
                setattr(config.thresholds, key, value)

    # 更新 weights
    if "weights" in data:
        for key, value in data["weights"].items():
            if hasattr(config.weights, key):
                setattr(config.weights, key, value)

    # 更新 safety
    if "safety" in data:
        for key, value in data["safety"].items():
            if hasattr(config.safety, key):
                setattr(config.safety, key, value)

    return config


def _print_report(report: dict, format_type: str):
    """打印报告"""
    stats = report.get("stats", {})

    print("\n" + "=" * 50)
    print("📊 执行报告")
    print("=" * 50)

    # 状态概览
    status_icon = "✅" if report["status"] == "completed" else "❌"
    mode_icon = "🔍" if report.get("dry_run") else "🚀"
    print(f"\n{status_icon} 状态: {report['status']}")
    print(f"{mode_icon} 模式: {'Dry-Run' if report.get('dry_run') else 'Live'}")
    print(f"⏱️  Run ID: {report['run_id']}")

    # 统计
    print("\n📈 统计:")
    print(f"   浅睡 - 扫描文件: {stats.get('files_scanned', 0)}")
    print(f"   浅睡 - 发现候选: {stats.get('candidates_found', 0)}")
    print(f"   REM  - 通过门槛: {stats.get('candidates_passed', 0)}")
    print(f"   REM  - Gene触发: {stats.get('genes_triggered', 0)}")
    print(f"   深睡 - 巩固记忆: {stats.get('consolidated', 0)}")
    print(f"   深睡 - 归档记忆: {stats.get('archived', 0)}")
    print(f"   深睡 - 胶囊创建: {stats.get('capsules_created', 0)}")

    # 安全提示
    if report.get("needs_human_review"):
        print("\n⚠️  需要人工审查")
    if report.get("backups_created", 0) > 0:
        print(f"💾  创建备份: {report['backups_created']} 个")

    # 错误信息
    if report.get("error"):
        print(f"\n❌ 错误: {report['error']}")

    print(f"\n📄 报告路径: {report.get('report_path', 'N/A')}")
    print()


def _print_evolution_status(workspace: Path):
    """打印进化状态"""
    print("\n" + "=" * 50)
    print("🧬 Gene/Capsule 进化状态")
    print("=" * 50)

    try:
        summary = get_evolution_status(str(workspace))

        # Gene 状态
        genes = summary.get("genes", {})
        print(f"\n🧪 Gene (基因):")
        print(f"   总数: {genes.get('total', 0)}")
        print(f"   启用: {genes.get('enabled', 0)}")
        print("   按类别:")
        for cat, count in genes.get("by_category", {}).items():
            print(f"      - {cat}: {count}")

        # Capsule 状态
        capsules = summary.get("capsules", {})
        print(f"\n💊 Capsule (胶囊):")
        print(f"   总数: {capsules.get('total', 0)}")
        print(f"   已验证: {capsules.get('validated', 0)}")

        # 事件统计
        events = summary.get("events", {})
        print(f"\n📝 Events (事件):")
        print(f"   内存中: {events.get('in_memory', 0)}")

        # 四层架构
        layers = summary.get("layers", {})
        print(f"\n📁 四层记忆架构:")
        print(f"   L1 索引: {layers.get('l1_index', 'N/A')}")
        print(f"   L2 事实: {layers.get('l2_facts', 'N/A')}")
        print(f"   L3 SOP:  {layers.get('l3_sops', 'N/A')}")
        print(f"   L4 原始: {layers.get('l4_raw', 'N/A')}")

    except Exception as e:
        print(f"\n⚠️ 获取进化状态失败: {e}")
        print("   提示: 请先运行一次记忆整合来初始化 Gene/Capsule 系统")


# ============================================================
# 模块入口
# ============================================================

if __name__ == "__main__":
    sys.exit(main())
