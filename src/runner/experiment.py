import json
import os
from src.core.config import Config
from src.core.types import GraphData
from src.envs.graph_env import GraphEnvironment
from src.memory.path_memory import PathMemory
from src.structure.macro import MacroStore
from src.structure.discovery import MacroDiscovery
from src.agents.random_agent import RandomAgent
from src.agents.macro_agent import MacroAgent


class ExperimentRunner:
    """
    实验运行器。
    负责组装所有组件，并执行主循环。
    """

    def __init__(self, config: Config):
        self.config = config

        # 1. 准备基础设施
        self.graph_data = self._load_graph(config.graph_file)
        self.env = GraphEnvironment(
            graph=self.graph_data,
            start=config.start_node,
            goal=config.goal_node
        )

        # 2. 准备大脑组件
        self.memory = PathMemory()
        self.macro_store = MacroStore()
        self.discovery = MacroDiscovery(config)

        # 3. 初始化 Agent
        # 这里我们演示：先用 RandomAgent 跑，或者直接用 MacroAgent
        # 为了体现"结构利用"，我们直接上 MacroAgent (它在没结构时会 fallback 到随机)
        self.agent = MacroAgent(config, self.memory, self.macro_store)

    def _load_graph(self, path: str) -> GraphData:
        """加载地图数据"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Graph file not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # 转换 JSON key 为 Tuple 列表格式 (符合 GraphData 类型定义)
        # JSON: { "A": [["B", 1.0], ["C", 2.0]] }
        # Python: { "A": [("B", 1.0), ("C", 2.0)] }
        graph: GraphData = {}
        for node, neighbors in raw_data.items():
            graph[node] = [(n[0], n[1]) for n in neighbors]

        return graph

    def run(self):
        """主循环"""
        print(f"🚀 Experiment Start! Episodes: {self.config.episodes}")
        print(f"🗺️  Map: {self.config.graph_file}")
        print("-" * 40)

        for ep in range(1, self.config.episodes + 1):
            # --- A. 跑一集 ---
            result = self.agent.run_episode(self.env)

            # --- B. 记入记忆 ---
            self.memory.add_episode(
                path=result["path"],
                cost=result["cost"],
                success=result["success"]
            )

            # --- C. 触发结构发现 ---
            # (可以在每集后触发，也可以每 N 集触发一次)
            self.discovery.discover(self.memory, self.macro_store)

            # --- D. 简单的日志输出 ---
            # 每 10 集打印一次，或者打印发现了宏的时候
            if ep % 10 == 0 or result["success"]:
                status = "✅" if result["success"] else "❌"
                macros_count = len(self.macro_store.get_all())
                print(
                    f"Ep {ep:03d} | {status} Cost: {result['cost']:.1f} | Steps: {result['steps']} | Macros: {macros_count}")

        self._print_summary()

    def _print_summary(self):
        print("\n" + "=" * 40)
        print("📊 Experiment Summary")
        print("=" * 40)

        macros = self.macro_store.get_all()
        print(f"🧠 Discovered Macros: {len(macros)}")
        for m in macros:
            print(f"  - Path: {m.path} | Used/Seen: {m.count} | AvgCost: {m.avg_cost:.2f}")

        print("\npath stats (top 3):")
        stats = self.memory.get_stats()
        # 按次数排序
        sorted_paths = sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)[:3]
        for p, s in sorted_paths:
            print(f"  - {list(p)}: {s['count']} times")