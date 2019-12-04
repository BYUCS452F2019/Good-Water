from datetime import datetime
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
            fountain_id: int,
    ) -> Tuple[int, Dict[str, Any]]:
        value = self.context.dao.get_average_rating(
            fountain_id=fountain_id,
        )

        return 200, {
            "fountainID": fountain_id,
            "fountainName": fountain_name,
            "averageValue": float(value) if value is not None else None,
        }

    def create_rating(
            self,
            fountain_name: str,
            fountain_id: int,
            rating: Dict[str, Any],
            token: Optional[str],
    ) -> Tuple[int, Dict[str, Any]]:
        user_id = self.context.authenticator.lookup_token(token)

        if user_id is None:
            return UNAUTHORIZED_RESPONSE

        value = rating["value"]

        if not 0 <= value <= 10:
            return 400, {
                "error": f"Invalid rating {value}",
            }

        print(f"Adding rating {value} to fountain {fountain_name}")

        self.context.dao.add_rating(
            score=value,
            timestamp=datetime.utcnow(),
            fountain_id=fountain_id,
            user_id=user_id,
        )

        return 200, {}

    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        fountain_name = params["fountain_name"]
        fountain = self.context.dao.lookup_fountain(
            fountain_name=fountain_name,
        )
        fountain_id = fountain["id"]

        if method == "GET":
            return self.get_rating(
                fountain_name=fountain_name,
                fountain_id=fountain_id,
            )
        elif method == "POST":
            return self.create_rating(
                fountain_name=fountain_name,
                fountain_id=fountain_id,
                rating=body["rating"],
                token=params["auth_token"],
            )
        else:
            return 400, {"error": "invalid method"}
