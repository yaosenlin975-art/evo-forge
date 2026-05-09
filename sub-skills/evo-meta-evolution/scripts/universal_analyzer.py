#!/usr/bin/env python3
"""
Darwin Meta-Evolution - 万能分析器
Universal Analyzer for all non-Skill/Agent/Code optimization targets
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


# ============================================================
# 1. 核心分析器类
# ============================================================

class UniversalAnalyzer:
    """万能分析器"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.type_strategies = {
            "memory": self.analyze_memory,
            "config": self.analyze_config,
            "doc": self.analyze_documentation,
            "structure": self.analyze_structure,
            "data": self.analyze_data,
            "container": self.analyze_container,
            "pipeline": self.analyze_pipeline,
            "schedule": self.analyze_schedule,
            "cross": self.analyze_cross_skill,
            "global": self.analyze_workspace_health,
            "generic": self.analyze_generic,
        }
    
    def analyze(self, target_type: str, target_path: Optional[str] = None) -> Dict:
        """主分析入口"""
        strategy = self.type_strategies.get(target_type, self.analyze_generic)
        return strategy(target_path)
    
    # ============================================================
    # 2. Memory 系统分析
    # ============================================================
    
    def analyze_memory(self, path: Optional[str] = None) -> Dict:
        """分析记忆系统"""
        path = path or str(self.workspace / "memory")
        memory_dir = Path(path)
        
        issues = []
        suggestions = []
        scores = {}
        
        # 检查 MEMORY.md
        memory_file = self.workspace / "MEMORY.md"
        if memory_file.exists():
            content = memory_file.read_text(encoding="utf-8")
            
            # 检查必含 section
            required_sections = [
                "用户资料", "工具设置", "重要决策", "经验教训"
            ]
            for section in required_sections:
                if section not in content:
                    issues.append({
                        "severity": "medium",
                        "type": "missing_section",
                        "detail": f"MEMORY.md 缺少「{section}」section"
                    })
            
            # 检查陈旧度
            last_modified = datetime.fromtimestamp(memory_file.stat().st_mtime)
            days_since_modified = (datetime.now() - last_modified).days
            if days_since_modified > 30:
                issues.append({
                    "severity": "high",
                    "type": "stale_info",
                    "detail": f"MEMORY.md 已 {days_since_modified} 天未更新"
                })
            
            scores["completeness"] = 85
            scores["consistency"] = 80
            scores["freshness"] = max(0, 100 - days_since_modified * 3)
        else:
            issues.append({
                "severity": "high",
                "type": "missing_file",
                "detail": "MEMORY.md 不存在"
            })
            scores["completeness"] = 20
        
        # 检查每日笔记
        if memory_dir.exists():
            daily_notes = list(memory_dir.glob("????-??-??.md"))
            if len(daily_notes) == 0:
                issues.append({
                    "severity": "medium",
                    "type": "no_daily_notes",
                    "detail": "memory/ 目录缺少每日笔记"
                })
            
            # 检查过期笔记
            old_notes = []
            for note in daily_notes:
                age = (datetime.now() - datetime.fromtimestamp(note.stat().st_mtime)).days
                if age > 30:
                    old_notes.append((note.name, age))
            
            if old_notes:
                suggestions.append({
                    "action": "archive_old_notes",
                    "detail": f"建议归档 {len(old_notes)} 个超过30天的旧笔记",
                    "files": [n[0] for n in old_notes]
                })
        
        return {
            "type": "memory",
            "scores": scores,
            "issues": issues,
            "suggestions": suggestions,
            "total_score": sum(scores.values()) / len(scores) if scores else 0
        }
    
    # ============================================================
    # 3. Config 文件分析
    # ============================================================
    
    def analyze_config(self, path: Optional[str] = None) -> Dict:
        """分析配置文件"""
        issues = []
        suggestions = []
        scores = {}
        
        config_files = []
        for pattern in ["*.json", "*.yaml", "*.yml", "*.toml", "*.ini", ".env*"]:
            config_files.extend(self.workspace.rglob(pattern))
        
        # 过滤掉 node_modules 等
        config_files = [f for f in config_files if "node_modules" not in str(f)]
        
        if not config_files:
            issues.append({
                "severity": "medium",
                "type": "no_config",
                "detail": "未找到配置文件"
            })
            return {"type": "config", "scores": {}, "issues": issues, "suggestions": [], "total_score": 0}
        
        # 安全检查
        secret_patterns = [
            (r'api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}', "API密钥"),
            (r'secret["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}', "密钥"),
            (r'password["\']?\s*[:=]\s*["\']?[^"\'\s]{8,}', "密码"),
            (r'aws[_-]?access[_-]?key', "AWS密钥"),
        ]
        
        for config_file in config_files:
            if config_file.name.startswith("."):
                continue  # 跳过隐藏文件
            
            try:
                content = config_file.read_text(encoding="utf-8", errors="ignore")
                
                for pattern, name in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append({
                            "severity": "critical",
                            "type": "secret_exposure",
                            "file": str(config_file),
                            "detail": f"{config_file.name} 可能包含明文{name}，应使用环境变量"
                        })
            except Exception as e:
                issues.append({
                    "severity": "low",
                    "type": "read_error",
                    "file": str(config_file),
                    "detail": f"无法读取: {str(e)}"
                })
        
        # 评分
        scores["security"] = 100 if not any(i["severity"] == "critical" for i in issues) else 20
        scores["completeness"] = 80
        scores["consistency"] = 75
        
        return {
            "type": "config",
            "files_found": [str(f) for f in config_files],
            "scores": scores,
            "issues": issues,
            "suggestions": suggestions,
            "total_score": sum(scores.values()) / len(scores) if scores else 0
        }
    
    # ============================================================
    # 4. 文档分析
    # ============================================================
    
    def analyze_documentation(self, path: Optional[str] = None) -> Dict:
        """分析文档"""
        issues = []
        suggestions = []
        scores = {}
        
        doc_files = []
        for pattern in ["README.md", "*.md", "docs/**/*.md", "doc/**/*.md"]:
            doc_files.extend(self.workspace.rglob(pattern))
        
        doc_files = [f for f in doc_files if "node_modules" not in str(f) and ".git" not in str(f)]
        
        if not doc_files:
            issues.append({
                "severity": "high",
                "type": "no_docs",
                "detail": "未找到文档"
            })
            return {"type": "doc", "scores": {}, "issues": issues, "suggestions": [], "total_score": 0}
        
        # 检查 README
        readme = self.workspace / "README.md"
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            
            checks = {
                "has_structure": len(re.findall(r'^#{1,3}\s+', content, re.MULTILINE)) > 0,
                "has_examples": "example" in content.lower() or "用法" in content,
                "has_install": "install" in content.lower() or "安装" in content,
            }
            
            for check, passed in checks.items():
                if not passed:
                    suggestions.append({
                        "action": check,
                        "detail": f"README 缺少「{check}」相关内容"
                    })
        else:
            issues.append({
                "severity": "high",
                "type": "no_readme",
                "detail": "缺少 README.md"
            })
        
        scores["completeness"] = 70 if readme.exists() else 30
        scores["structure"] = 75
        
