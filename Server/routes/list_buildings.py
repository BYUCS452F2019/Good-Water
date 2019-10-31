from typing import Any, Dict, Optional, Tuple

from routes.route import Route


class ListBuildingsRoute(Route):
    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        if method != "GET":
            return 400, {"error": "invalid method"}

        return 200, {"buildings": ["JFSB"]}
