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

        buildings = self.context.dao.list_buildings()

        return 200, {
            "buildings": [
                {
                    "id": b["id"],
                    "name": b["name"],
                    "latitude": b["latitude"],
                    "longitude": b["longitude"],
                } for b in buildings
            ],
        }
