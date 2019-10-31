from typing import Any, Dict, Optional, Tuple

from context import ServerContext
from routes.route import Route


class LoginRoute(Route):
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

        token = self.context.authenticator.create_token(
            body["username"],
            body["password"],
        )

        if token is not None:
            return 200, {
                "token": token,
            }
        else:
            return 401, {
                "error_id": "INVALID_CREDENTIALS",
                "error": "Incorrect username or password",
            }
