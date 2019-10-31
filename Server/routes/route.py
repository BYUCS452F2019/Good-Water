from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class Route(ABC):
    @abstractmethod
    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        pass
