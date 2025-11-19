import typing
from typing import List, Dict, Tuple, Any, Union, NewType
from dataclasses import dataclass

# ==========================================
# 基础语义类型 (Type Aliases)
# ==========================================

# 节点 ID：为了方便阅读和 JSON 序列化，我们统一用字符串
NodeID = str

# 代价/消耗：浮点数
Cost = float

# 状态：目前图环境里 State = NodeID，但为了以后扩展（比如 GridWorld 的坐标），
# 我们保留 State 这个概念
State = Any

# 动作：在简单图里 Action 就是“下一个 NodeID”，但保留泛型能力
Action = Any

# ==========================================
# 复合数据结构
# ==========================================

# 路径：按顺序经过的一系列节点
Path = List[NodeID]

# 图的原始数据结构 (Adjacency List)
# 格式: { "StartNode": [("TargetNode", Cost), ...], ... } 这里以后可能还是要注意的
GraphData = Dict[NodeID, List[Tuple[NodeID, Cost]]]

# ==========================================
# 交互协议 (Interaction Protocol)
# ==========================================

@dataclass(frozen=True)
class StepResult:
    """
    Environment.step() 的标准返回结果。
    使用 dataclass 而不是 tuple，是为了以后代码可读性更好。
    """
    next_state: State      # 执行动作后的新状态
    cost: Cost             # 本次动作的消耗 (负奖励)
    done: bool             # 是否到达终点或结束
    info: Dict[str, Any]   # 额外的调试信息 (比如 'invalid_move': True)