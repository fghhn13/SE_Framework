import sys
import os

# ==========================================
# 路径黑魔法 (Path Magic) 🧙‍♀️
# ==========================================
# 获取当前脚本所在的目录 (scripts/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录 (project_root/)
project_root = os.path.dirname(current_dir)
# 将项目根目录加入 Python 的搜索路径
if project_root not in sys.path:
    sys.path.append(project_root)

# ==========================================
# 正常导入
# ==========================================
from src.core.config import Config
from src.runner.experiment import ExperimentRunner


def main():
    # 1. 确定配置文件路径
    # 假设默认配置文件在 config/default.json
    config_path = os.path.join(project_root, "config", "default.json")

    # 2. 加载配置
    # 如果文件不存在，Config 类会自动使用默认值
    config = Config.from_json(config_path)

    # --- 临时修正路径 ---
    # 为了防止路径写死导致找不到文件，我们在这里强制把 graph_file
    # 指向项目根目录下的 data/graphs/toy_graph.json
    # (这样你不用去改 config json 也能跑)
    target_graph_file = os.path.join(project_root, "data", "graphs", "toy_graph.json")
    config.graph_file = target_graph_file

    # 确保数据目录存在 (贴心小助手)
    os.makedirs(os.path.dirname(target_graph_file), exist_ok=True)

    print(f"🔧 Config loaded. Episodes: {config.episodes}")

    # 3. 启动实验
    try:
        runner = ExperimentRunner(config)
        runner.run()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   (Tip: Did you create the graph JSON file yet?)")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()