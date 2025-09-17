from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):

    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def input_schema(self) -> dict[str, Any]:
        pass

    @property
    def schema(self) -> dict[str, Any]:
        """Provides tools JSON Schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema
            }
        }