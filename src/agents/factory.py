from src.core.config import Config
from src.memory.path_memory import PathMemory
from src.structure.macro import MacroStore
from src.agents.base import Agent
from src.agents.random_agent import RandomAgent
from src.agents.macro_agent import MacroAgent

class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str, config: Config, memory: PathMemory, store: MacroStore) -> Agent:
        """
        根据类型字符串创建 Agent 实例
        """
        if agent_type == "random":
            return RandomAgent(config, memory, store)
        elif agent_type == "macro":
            return MacroAgent(config, memory, store)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")