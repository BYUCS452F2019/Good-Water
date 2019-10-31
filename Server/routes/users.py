from typing import Any, Dict, Optional, Tuple

from context import ServerContext
from routes.route import Route


class UsersRoute(Route):
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
        if method != "POST":
            return 400, {"error": "invalid method"}

        email = body["email"]
        password = body["password"]

        # TODO: use the DAO to actually create a new user if possible
        user_id = "123"

        return 200, {
            "user_id": user_id,
        }
