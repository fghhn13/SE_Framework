import sys
import os
import argparse

# ==========================================
# 路径黑魔法 (Path Magic) 🧙‍♀️
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# ==========================================
# 正常导入
# ==========================================
from src.core.config import Config
from src.runner.experiment import ExperimentRunner


def main():
    # 1. 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=str, default="0000", help="Map ID")
    parser.add_argument("--agent", type=str, default="default", help="Agent ID (Name of the folder)")

    # --- 新增参数 ---
    parser.add_argument("--type", type=str, default="macro", choices=["macro", "random"], help="Agent strategy type")

    parser.add_argument("--episodes", type=int, default=None)
    args = parser.parse_args()

    # 2. 构造地图路径
    # 确保 ID 是 4 位数 (比如输入 1 会变成 0001)
    map_id = args.map.zfill(4)
    map_filename = f"{map_id}.json"
    map_path = os.path.join(project_root, "data", "graphs", map_filename)

    # 3. 加载基础配置
    config_path = os.path.join(project_root, "config", "default.json")
    config = Config.from_json(config_path)

    # 4. 动态覆盖配置
    print(f"🎯 Target Map: {map_filename}")

    if not os.path.exists(map_path):
        print(f"❌ Error: Map file not found: {map_path}")
        print(f"   (Please ask AI to generate '{map_filename}' and put it in data/graphs/)")
        return

    config.graph_file = map_path

    # 如果命令行指定了 episode 数量，覆盖 config 里的
    if args.episodes:
        config.episodes = args.episodes

    print(f"🔧 Config loaded. Episodes: {config.episodes}")

    # 5. 启动实验
    try:
        # 传入 agent_type
        runner = ExperimentRunner(
            config,
            agent_id=args.agent,
            agent_type=args.type  # <--- 传入参数
        )
        runner.run()
    except Exception as e:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()