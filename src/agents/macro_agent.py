import random
from typing import Dict, Any
from src.core.types import Path
from src.envs.base import Environment
from .base import Agent


class MacroAgent(Agent):
    """
    结构利用型 Agent。
    优先尝试匹配 MacroStore 中的宏结构。
    """

    def run_episode(self, env: Environment) -> Dict[str, Any]:
        state = env.reset()

        path: Path = [state]
        total_cost = 0.0
        steps = 0
        success = False

        while steps < self.config.max_steps:
            # A. 检查当前状态是否有可用的 Macro
            applicable_macros = self.structure_store.find_applicable(state)

            # B. 决策：使用 Macro 还是随机探索？
            # 逻辑：如果有宏，且随机数大于 explore_prob (利用)，则使用宏
            use_macro = False
            selected_macro = None

            if applicable_macros and random.random() > self.config.explore_prob:
                # 简单策略：选择平均代价最小的 Macro
                # (以后这里可以是更复杂的 Policy)
                selected_macro = min(applicable_macros, key=lambda m: m.avg_cost)
                use_macro = True

            if use_macro and selected_macro:
                # --- 模式 1: 执行宏 (连续执行多步) ---
                # Macro.path 比如是 ['A', 'B', 'C']
                # 当前在 'A'。我们需要依次执行 A->B, B->C

                macro_path = selected_macro.path
                # 从索引 1 开始，因为索引 0 是当前位置
                for next_node_in_macro in macro_path[1:]:

                    # 防御性检查：宏说能走，但环境允许吗？
                    # (防止环境变了宏还没更新的情况)
                    valid_actions = env.get_actions(state)
                    if next_node_in_macro not in valid_actions:
                        # 宏失效了！中断执行，退化为单步
                        break

                    # 执行宏里的一步
                    result = env.step(state, next_node_in_macro)

                    state = result.next_state
                    path.append(state)
                    total_cost += result.cost
                    steps += 1

                    if result.done:
                        success = True
                        break

                if success:
                    break

            else:
                # --- 模式 2: 随机单步 (Fallback) ---
                actions = env.get_actions(state)
                if not actions:
                    break

                action = random.choice(actions)
                result = env.step(state, action)

                state = result.next_state
                path.append(state)
                total_cost += result.cost
                steps += 1

                if result.done:
                    success = True
                    break

        return {
            "path": path,
            "cost": total_cost,
            "success": success,
            "steps": steps
        }