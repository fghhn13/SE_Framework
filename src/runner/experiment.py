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

    def __init__(self, config: Config, agent_id: str = "default_agent"):
        self.config = config
        self.agent_id = agent_id

        # 1. 准备环境
        # (这里假设你之前的 _load_graph 方法还在，为了节省篇幅省略细节)
        self.graph_data = self._load_graph(config.graph_file)
        self.env = GraphEnvironment(self.graph_data, config.start_node, config.goal_node)

        # 2. 准备大脑组件
        self.memory = PathMemory()
        self.macro_store = MacroStore()
        self.discovery = MacroDiscovery(config)

        # --- 关键：确定存档路径 ---
        # data/agents/{agent_id}/
        self.agent_dir = os.path.join("data", "agents", self.agent_id)
        os.makedirs(self.agent_dir, exist_ok=True)

        self.memory_file = os.path.join(self.agent_dir, "memory.json")
        self.macro_file = os.path.join(self.agent_dir, "macros.json")

        # --- 关键：加载旧档 ---
        print(f"📂 Agent Profile: {self.agent_id}")
        self.memory.load(self.memory_file)
        self.macro_store.load(self.macro_file)

        # 3. 初始化 Agent
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
        print(f"🚀 Experiment Start! Episodes: {self.config.episodes}")
        print(f"📂 Agent: {self.agent_id}")
        print("-" * 40)

        try:
            # --- 主循环开始 ---
            for ep in range(1, self.config.episodes + 1):
                # 1. 跑一集
                result = self.agent.run_episode(self.env)

                # 2. 记入记忆
                self.memory.add_episode(
                    path=result["path"],
                    cost=result["cost"],
                    success=result["success"]
                )

                # 3. 触发结构发现
                self.discovery.discover(self.memory, self.macro_store)

                # 4. 打印日志
                if ep % 10 == 0 or (result["success"] and ep < 5):
                    macros_count = len(self.macro_store.get_all())
                    print(
                        f"Ep {ep:03d} | Cost: {result['cost']:.1f} | Steps: {result['steps']} | Macros: {macros_count}")
            # --- 主循环结束 ---

        except KeyboardInterrupt:
            # 如果你在终端按了 Ctrl+C，会跳到这里
            print("\n⚠️  Experiment interrupted by user! Stopping...")

        except Exception as e:
            # 捕获其他意外报错
            print(f"\n❌ Unexpected Error: {e}")
            import traceback
            traceback.print_exc()

        finally:

            print("\n" + "=" * 40)
            print("💾 Saving Agent State...")
            self.memory.save(self.memory_file)
            self.macro_store.save(self.macro_file)
            print(f"   -> Saved to {self.agent_dir}")

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