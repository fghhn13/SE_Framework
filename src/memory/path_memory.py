from collections import defaultdict
from typing import List, Dict, Any, Tuple
from src.core.types import Path, Cost


class PathMemory:
    """
    路径记忆模块。
    负责记录 Agent 走过的所有路径，并统计它们的出现频率和代价值。
    """

    def __init__(self):
        # 核心存储结构
        # Key: 路径 (tuple 形式，因为 list 不可哈希)
        # Value: 统计数据 (出现次数、总消耗、成功次数)
        self.path_stats = defaultdict(lambda: {
            "count": 0,
            "total_cost": 0.0,
            "success_count": 0
        })

    def add_episode(self, path: Path, cost: Cost, success: bool):
        """
        记录一次完整的 Episode。
        """
        if not path:
            return

        # 将 list 转换为 tuple，因为字典的 key 必须是不可变的
        path_key = tuple(path)

        stats = self.path_stats[path_key]
        stats["count"] += 1
        stats["total_cost"] += cost
        if success:
            stats["success_count"] += 1

    def get_stats(self) -> Dict[Tuple[str, ...], Dict[str, Any]]:
        """
        获取原始统计数据。
        结构发现模块 (Discovery) 会调用这个接口来挖掘模式。
        """
        return self.path_stats

    def get_best_path(self) -> Path:
        """
        (Helper) 从记忆中检索一条“只要成功过、且平均代价最低”的路径。
        供 ReplayAgent 使用。
        """
        best_path = []
        min_avg_cost = float('inf')

        for path_tuple, stats in self.path_stats.items():
            # 只考虑成功过的路径
            if stats["success_count"] > 0:
                avg_cost = stats["total_cost"] / stats["count"]

                # 寻找代价最小的
                if avg_cost < min_avg_cost:
                    min_avg_cost = avg_cost
                    best_path = list(path_tuple)

        return best_path

    def clear(self):
        """清空记忆"""
        self.path_stats.clear()