from abc import ABC, abstractmethod
from typing import Dict, Any
from src.core.config import Config
from src.memory.path_memory import PathMemory
from src.structure.macro import MacroStore
from src.envs.base import Environment

class Agent(ABC):
    """
    Agent 基类。
    持有 Config, Memory 和 StructureStore 的引用。
    """
    def __init__(self, config: Config, memory: PathMemory, structure_store: MacroStore):
        self.config = config
        self.memory = memory
        self.structure_store = structure_store

    @abstractmethod
    def run_episode(self, env: Environment) -> Dict[str, Any]:
        """
        在环境中运行一次完整的 Episode。
        Returns:
            Dict: 包含 path, cost, success 等信息的字典
        """
        pass