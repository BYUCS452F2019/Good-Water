from typing import Any, Dict, Optional, Tuple

from routes.route import Route


class ListFountainsRoute(Route):
    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        if method != "GET":
            return 400, {"error": "invalid method"}

        building_name = params["building_name"]
        # TODO: return fountains in building named `building_name`

        return 200, {"fountains": [f"{building_name}_fountain1"]}
