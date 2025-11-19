from src.core.config import Config
from src.memory.path_memory import PathMemory
from .macro import MacroStore, Macro


class MacroDiscovery:
    """
    结构发现器 (Structure Discovery)
    定期查看记忆，提取高频模式。
    """

    def __init__(self, config: Config):
        self.threshold = config.macro_threshold

    def discover(self, memory: PathMemory, store: MacroStore):
        """
        核心算法：从 PathMemory 中挖掘 Macro 并存入 MacroStore。
        """
        stats = memory.get_stats()

        for path_tuple, info in stats.items():
            count = info["count"]

            # 1. 过滤：只提取出现次数超过阈值的路径
            if count >= self.threshold:

                # 2. 过滤：这里只提取成功的路径 (可选策略)
                # 如果你希望提取"经常走的坑"，可以去掉这个判断
                if info["success_count"] == 0:
                    continue

                avg_cost = info["total_cost"] / count

                # 3. 构建 Macro 对象
                new_macro = Macro(
                    path=list(path_tuple),
                    avg_cost=avg_cost,
                    count=count
                )

                # 4. 存入仓库
                store.add_macro(new_macro)