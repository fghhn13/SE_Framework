import json
import os
from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class Config:
    """
    全局配置类 (Global Configuration)
    所有可调整的参数都在这里定义，避免魔法数字 (Magic Numbers) 散落在代码各处。
    """

    # ==========================
    # 1. 实验控制 (Experiment)
    # ==========================
    episodes: int = 100  # 跑多少集 (Episodes)
    max_steps: int = 50  # 每一集最多走多少步 (防止死循环)
    random_seed: int = 42  # 随机种子 (复现实验用)
    output_dir: str = "results"  # 结果输出目录

    # ==========================
    # 2. 环境设置 (Environment)
    # ==========================
    graph_file: str = "data/graphs/toy_graph.json"  # 地图文件路径
    start_node: str = "A"  # 起点
    goal_node: str = "F"  # 终点 (目标)

    # ==========================
    # 3. Agent 与 结构参数
    # ==========================
    explore_prob: float = 0.1  # 随机探索概率 (epsilon)
    macro_threshold: int = 5  # 结构涌现阈值：路径重复多少次后变成 Macro

    @classmethod
    def from_json(cls, json_path: str) -> 'Config':
        """
        从 JSON 文件加载配置。
        如果文件不存在，或者字段缺失，会自动使用上面的默认值。
        """
        if not os.path.exists(json_path):
            print(f"[Config] Warning: Config file '{json_path}' not found. Using defaults.")
            return cls()

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 过滤掉 JSON 中多余的 key，防止 dataclass 报错
        # (这样以后你在 JSON 里写注释或者废弃字段，代码也不会崩)
        valid_keys = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}

        print(f"[Config] Loaded configuration from {json_path}")
        return cls(**filtered_data)


# 用于测试的小入口
if __name__ == "__main__":
    # 假装加载一下，看看默认值
    cfg = Config.from_json("non_existent_file.json")
    print(f"Default Episodes: {cfg.episodes}")
    print(f"Default Start Node: {cfg.start_node}")