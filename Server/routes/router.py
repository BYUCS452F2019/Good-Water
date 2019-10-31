import re
from typing import Any, Dict, Optional, Tuple

from routes.route import Route


class Router(Route):
    routes: Dict[str, Route]
    param_name: Optional[str]
    param_route: Optional[Route]

    def __init__(self, routes: Dict[str, Route]):
        routes = dict(routes)
        pattern = r"<([^<>]+)>"

        param_routes = [
            r for r in routes if re.match(pattern, r)
        ]

        assert len(param_routes) <= 1

        if len(param_routes) == 0:
            self.param_name = None
            self.param_route = None
        else:
            self.param_name = re.findall(pattern, param_routes[0])[0]
            self.param_route = routes[param_routes[0]]
            del routes[param_routes[0]]

        self.routes = routes

    def handle(
            self,
            path: str,
            method: str,
            body: Optional[Dict[str, Any]],
            params: Dict[str, str],
    ) -> Tuple[int, Dict[str, Any]]:
        params = dict(params)
        split_path = path.split("/", 1)

        if len(split_path) == 1:
            split_path.append("")

        current, remaining = split_path

        if current in self.routes:
            route = self.routes[current]
        elif self.param_route is not None:
            route = self.param_route
            params[self.param_name] = current
        else:
            return 404, {}

        return route.handle(
            path=remaining,
            method=method,
            params=params,
            body=body,
        )
