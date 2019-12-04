from typing import Any, Dict, Optional, Tuple

from context import ServerContext
from routes.route import Route


class ListCampusesRoute(Route):
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

        campuses = self.context.dao.list_campuses()

        return 200, {
            "campuses": [
                {
                    "id": c["id"],
                    "name": c["name"],
                    "city": c["city"],
                    "state": c["state"],
                } for c in campuses
            ],
        }
