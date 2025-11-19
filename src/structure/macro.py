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
    count: int  # 被发现/使用的次数 (置信度)

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
        """
        添加一个宏。
        (未来可以在这里做去重、合并逻辑)
        """
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

    # --- 新增：读档功能 ---
    def load(self, filepath: str):
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        self.macros = [Macro(**item) for item in raw_data]
        print(f"[Structure] Loaded {len(self.macros)} macros.")