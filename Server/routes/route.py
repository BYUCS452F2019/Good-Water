from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

UNAUTHORIZED_RESPONSE = 401, {"error": "Not Authorized."}


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
