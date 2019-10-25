from abc import ABC, abstractmethod
from typing import List

from context import ClientContext


class CommandHandler(ABC):
    """Abstract base class for command handlers."""
    command_name: str
    context: ClientContext

    def run(self, argv: List[str]):
        pass
