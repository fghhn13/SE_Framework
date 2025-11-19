import json
import os
from dataclasses import dataclass, asdict
from typing import List
from src.core.types import Path, NodeID, Cost


@dataclass
class Macro:
    """
    宏结构 (Macro)
    代表一段固化的、可重用的行为序列。
    比如：从 A 到 C，不用一步步走，直接调用 Macro(A->B->C)。
    """
    path: Path  # 宏包含的节点序列 [Start, ..., End]
    avg_cost: Cost  # 这条宏的平均代价
    count: float  # 被发现/使用的次数 (置信度)
    last_used: int = 0
    @property
    def start_node(self) -> NodeID:
        return self.path[0] if self.path else ""

    @property
    def end_node(self) -> NodeID:
        return self.path[-1] if self.path else ""


class MacroStore:
    """
    宏仓库 (Macro Store)
    负责存储所有的宏，并提供检索接口。
    """

    def __init__(self):
        self.macros: List[Macro] = []

    def add_macro(self, macro: Macro):

        # 简单查重：如果完全一样的路径已经存在，就更新数据
        for m in self.macros:
            if m.path == macro.path:
                m.count = macro.count
                m.avg_cost = macro.avg_cost
                return

        self.macros.append(macro)
        print(f"[MacroStore] New structure discovered: {macro.path} (Cost: {macro.avg_cost:.2f})")

    def find_applicable(self, current_node: NodeID) -> List[Macro]:
        """
        查找当前节点能用的所有宏。
        """
        return [m for m in self.macros if m.start_node == current_node]

    def get_all(self) -> List[Macro]:
        return self.macros

    def save(self, filepath: str):
        data = [asdict(m) for m in self.macros]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    # --- 读档功能 ---
    def load(self, filepath: str):
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        self.macros = [Macro(**item) for item in raw_data]
        print(f"[Structure] Loaded {len(self.macros)} macros.")

    # --- 新增：惩罚机制 ---
    def punish(self, macro_path: Path, penalty: float):
        """
        当宏执行失败时调用。大幅降低其置信度。
        """
        for m in self.macros:
            if m.path == macro_path:
                m.count = max(0.0, m.count - penalty)
                print(f"📉 Macro Punished! {m.path} -> Count: {m.count:.2f}")
                return

    # --- 新增：衰减与清理机制 ---
    def decay_and_prune(self, decay_rate: float, prune_threshold: float):
        """
        每一集结束调用。
        1. 所有宏的 count * decay_rate
        2. 移除 count < threshold 的宏
        """
        # 1. 衰减
        for m in self.macros:
            m.count *= decay_rate

        # 2. 统计之前的数量
        before_count = len(self.macros)

        # 3. 剔除弱者 (保留 count >= 阈值的)
        self.macros = [m for m in self.macros if m.count >= prune_threshold]

        removed_count = before_count - len(self.macros)
        if removed_count > 0:
            print(f"♻️  Forgot {removed_count} obsolete macros.")