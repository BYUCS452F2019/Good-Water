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

        username = body["username"]
        password = body["password"]
        first_name = body["firstName"]
        last_name = body["lastName"]

        # TODO handle errors/user already existing

        self.context.dao.add_user(
            user_name=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        return 200, {}
