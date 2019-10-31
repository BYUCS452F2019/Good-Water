import http.server
import json
import socketserver
import traceback

from authenticator import Authenticator
from dao.dao import DAO
from context import ServerContext
from routes.list_buildings import ListBuildingsRoute
from routes.list_fountains import ListFountainsRoute
from routes.login import LoginRoute
from routes.ratings import RatingsRoute
from routes.router import Router
from routes.users import UsersRoute

PORT = 8080

router = None


class Handler(http.server.SimpleHTTPRequestHandler):
    def _handle(self, method):
        global router
        content_len = int(self.headers.get("Content-Length", failobj="0"))

        if content_len == 0:
            body = None
        else:
            body = json.loads(self.rfile.read(content_len))

        auth_token = self.headers.get("Auth-Token", failobj=None)

        params = {
            "auth_token": auth_token
        }

        try:
            status, response = router.handle(
                path=self.path.split("/", 1)[-1],
                method=method,
                body=body,
                params=params,
            )
        except Exception as ex:
            traceback.print_exc()
            trace = traceback.format_exc()
            status, response = 500, {
                "error": trace,
            }

        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf8"))

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def do_PUT(self):
        self._handle("PUT")

    def do_DELETE(self):
        self._handle("DELETE")


def main():
    global router
    dao = DAO()
    authenticator = Authenticator(
        dao=dao,
    )

    try:
        dao.connect_to_database()
    except Exception as ex:
        # TODO: get rid of this or handle more specific exception
        # this is here just to make it easier to test dummy methods
        traceback.print_exc()

    context = ServerContext(
        authenticator=authenticator,
        dao=dao,
    )

    router = Router({
        "buildings": Router({
            "": ListBuildingsRoute(context),
            "<building_name>": Router({
                "fountains": Router({
                    "": ListBuildingsRoute(context),
                    "<fountain_id>": Router({
                        "ratings": RatingsRoute(context),
                    }),
                }),
            }),
        }),
        "login": LoginRoute(context),
        "users": UsersRoute(context),
    })

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)

        try:
            httpd.serve_forever()
        finally:
            dao.disconnect_from_database()

        # This class is responsible for making API endpoints that
        # will receive JSON objects and then call DAO methods such as "addUser"
        # "addBuildling" etc.


if __name__ == "__main__":
    main()
