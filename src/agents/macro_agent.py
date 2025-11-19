import random
from typing import Dict, Any
from src.core.types import Path
from src.envs.base import Environment
from .base import Agent


class MacroAgent(Agent):
    """
    结构利用型 Agent (势利眼版)。
    会根据宏的“性价比”决定是信任它还是去探索。
    """

    def run_episode(self, env: Environment) -> Dict[str, Any]:
        state = env.reset()

        path: Path = [state]
        total_cost = 0.0
        steps = 0
        success = False
        macros_used = 0  # 统计宏使用次数

        while steps < self.config.max_steps:
            # A. 检查当前状态是否有可用的 Macro
            applicable_macros = self.structure_store.find_applicable(state)

            use_macro = False
            selected_macro = None

            # ============================================================
            # 🧠 核心改动：势利眼逻辑 (Snobby Logic)
            # ============================================================
            if applicable_macros:
                # 1. 先挑出那个“目前看来最好”的宏 (Best Candidate)
                best_macro = min(applicable_macros, key=lambda m: m.avg_cost)

                # 2. 计算动态探索率 (Dynamic Epsilon)
                # 设定心中的"基准价格"，比如 3.0。
                # Cost < 3.0 -> 便宜 -> 降低探索率 (信任)
                # Cost > 3.0 -> 贵   -> 提高探索率 (怀疑)
                benchmark_cost = 8.0
                cost_ratio = best_macro.avg_cost / benchmark_cost

                # 基础概率 * 价格系数
                dynamic_epsilon = self.config.explore_prob * cost_ratio

                # 3. 钳位 (Clamp) 防止概率失控
                # 最低 0.5% (保留一丝好奇心), 最高 50% (不能全是瞎走)
                dynamic_epsilon = max(0.005, min(0.5, dynamic_epsilon))

                # 4. 决策
                # 只有当 随机数 > 动态Epsilon 时，才利用宏 (Exploit)
                if random.random() > dynamic_epsilon:
                    selected_macro = best_macro
                    use_macro = True
            # ============================================================

            if use_macro and selected_macro:
                # --- 模式 1: 执行宏 (连续执行多步) ---
                macros_used += 1  # 记录使用次数

                macro_path = selected_macro.path
                macro_failed = False  # 标记一下失败

                # 从索引 1 开始，因为索引 0 是当前位置
                for next_node_in_macro in macro_path[1:]:

                    # 防御性检查：宏说能走，但环境允许吗？
                    valid_actions = env.get_actions(state)
                    if next_node_in_macro not in valid_actions:
                        macro_failed = True
                        break  # 中断

                    # 执行
                    result = env.step(state, next_node_in_macro)

                    state = result.next_state
                    path.append(state)
                    total_cost += result.cost
                    steps += 1

                    if result.done:
                        success = True
                        break

                if macro_failed:
                    # 告诉 StructureStore 惩罚这个宏
                    self.structure_store.punish(selected_macro.path, self.config.failure_penalty)
                    # 继续 fallback 到下一次循环的逻辑

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
            "steps": steps,
            "macros_used": macros_used  # 返回宏使用次数，方便画图分析
        }