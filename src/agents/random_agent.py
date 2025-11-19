import random
from typing import Dict, Any
from src.core.types import Path
from src.envs.base import Environment
from .base import Agent


class RandomAgent(Agent):
    """
    完全随机的 Agent。
    不使用 Memory，也不查看 Structure。
    """

    def run_episode(self, env: Environment) -> Dict[str, Any]:
        # 1. 重置环境
        state = env.reset()

        path: Path = [state]
        total_cost = 0.0
        steps = 0
        success = False

        # 2. 循环步进
        while steps < self.config.max_steps:
            # 获取可选动作
            actions = env.get_actions(state)

            # 死胡同检查
            if not actions:
                break

                # --- 决策核心：纯随机 ---
            action = random.choice(actions)
            # -----------------------

            # 执行动作
            result = env.step(state, action)

            # 更新状态
            state = result.next_state
            path.append(state)
            total_cost += result.cost
            steps += 1

            # 检查是否结束
            if result.done:
                success = True
                break

        return {
            "path": path,
            "cost": total_cost,
            "success": success,
            "steps": steps
        }