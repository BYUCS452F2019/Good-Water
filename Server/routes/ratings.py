from typing import Any, Dict, Optional, Tuple

from context import ServerContext
from routes.route import Route, UNAUTHORIZED_RESPONSE


class RatingsRoute(Route):
    context: ServerContext

    def __init__(self, context: ServerContext):
        self.context = context

    def get_rating(
            self,
            fountain_name: str,
    ) -> Tuple[int, Dict[str, Any]]:
        return 200, {
            "fountain": fountain_name,
            "averageValue": 3.5,
        }

    def create_rating(
            self,
            fountain_name: str,
            rating: Dict[str, Any],
            token: Optional[str],
    ) -> Tuple[int, Dict[str, Any]]:
        user_id = self.context.authenticator.lookup_token(token)

        if user_id is None:
            return UNAUTHORIZED_RESPONSE

        value = rating["value"]

        if not 0.0 <= value <= 5.0:
            return 400, {
                "error": f"Invalid rating {value}",
            }

        print(f"Adding rating {value} to fountain {fountain_name}")

        # TODO: add the rating

        return 200, {}

    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        fountain_name = params["fountain_name"]

        if method == "GET":
            return self.get_rating(
                fountain_name=fountain_name,
            )
        elif method == "POST":
            return self.create_rating(
                fountain_name=fountain_name,
                rating=body["rating"],
                token=params["auth_token"],
            )
        else:
            return 400, {"error": "invalid method"}
