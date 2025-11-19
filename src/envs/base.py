from abc import ABC, abstractmethod
from typing import List, Any
from src.core.types import State, Action, StepResult

class Environment(ABC):
    """
    环境抽象基类 (Abstract Base Class)
    规定了 Agent 和环境交互的标准接口。
    """

    @abstractmethod
    def reset(self) -> State:
        """
        重置环境到初始状态。
        Returns:
            Initial state
        """
        pass

    @abstractmethod
    def get_actions(self, state: State) -> List[Action]:
        """
        获取当前状态下所有合法的动作。
        """
        pass

    @abstractmethod
    def step(self, state: State, action: Action) -> StepResult:
        """
        执行动作，环境发生变化。
        Returns:
            StepResult (next_state, cost, done, info)
        """
        pass