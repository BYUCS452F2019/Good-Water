from typing import Any, Dict, Optional, Tuple

from context import ServerContext
from routes.route import Route


class ListFountainsRoute(Route):
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

        building_name = params["building_name"].upper()
        # TODO: return fountains in building named `building_name`

        return 200, {
            "fountains": [
                {
                    "building": building_name,
                    "id": "fountain1",
                },
                {
                    "building": building_name,
                    "id": "fountain2",
                },
            ]
        }
