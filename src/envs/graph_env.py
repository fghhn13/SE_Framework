from typing import List, Tuple
from src.core.types import State, Action, StepResult, GraphData, NodeID, Cost
from .base import Environment


class GraphEnvironment(Environment):
    def __init__(self, graph: GraphData, start: NodeID, goal: NodeID):
        self.graph = graph
        self.start_node = start
        self.goal_node = goal

    def reset(self) -> State:
        return self.start_node

    def get_actions(self, state: State) -> List[Action]:
        # 在图里，Action 就是“下一个节点的 ID”
        # self.graph.get(state, []) 返回的是 [(neighbor, cost), ...]
        # 我们只提取 neighbor 作为 action
        neighbors = self.graph.get(state, [])
        return [node for (node, cost) in neighbors]

    def step(self, state: State, action: Action) -> StepResult:
        """
        在图上移动一步。
        action: 目标节点的 ID (NodeID)
        """
        candidates = self.graph.get(state, [])

        # 查找 action 是否在邻居列表中
        # 格式: candidates = [("B", 1.0), ("C", 5.0)]
        match = [c for c in candidates if c[0] == action]

        if not match:
            # 非法动作处理：原地不动，给予巨大惩罚（可选），或者标记 done
            # 这里我们简单处理：原地不动，cost=0，但在 info 里报错
            return StepResult(
                next_state=state,
                cost=0.0,
                done=True,  # 或者 False，看你是否允许非法动作继续
                info={"error": f"Invalid transition from {state} to {action}"}
            )

        next_node, cost = match[0]

        # 判断是否到达终点
        is_done = (next_node == self.goal_node)

        return StepResult(
            next_state=next_node,
            cost=cost,
            done=is_done,
            info={}
        )