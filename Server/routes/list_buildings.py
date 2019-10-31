from typing import Any, Dict, Optional, Tuple

from context import ServerContext
from routes.route import Route


class ListBuildingsRoute(Route):
    context: ServerContext

    def __init__(self, context: ServerContext):
        self.context = context

    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        if method != "GET":
            return 400, {"error": "invalid method"}

        return 200, {
            "buildings": [
                {
                    "name": "JFSB",
                    "latitude": 1,
                    "latitude": 2,
                },
                {
                    "name": "TMCB",
                    "latitude": 3,
                    "latitude": 4,
                },
            ],
        }
