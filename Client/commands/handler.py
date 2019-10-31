from abc import ABC, abstractmethod
from typing import List

from context import ClientContext


class CommandHandler(ABC):
    """Abstract base class for command handlers."""
    command_name: str
    help_text: str
    context: ClientContext

    @abstractmethod
    def run(self, argv: List[str]):
        pass
