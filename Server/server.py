import http.server
import json
import socketserver
import traceback
import urllib.parse

from authenticator import Authenticator
from dao.mongodao import MongoDAO
from context import ServerContext
from routes.list_buildings import ListBuildingsRoute
from routes.list_campuses import ListCampusesRoute
from routes.list_fountains import ListFountainsRoute
from routes.login import LoginRoute
from routes.ratings import RatingsRoute
from routes.router import Router
from routes.users import UsersRoute
from utils import relative

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

        path = urllib.parse.unquote(self.path)

        if path[0] == "/":
            path = path[1:]

        try:
            status, response = router.handle(
                path=path,
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


def create_dao() -> MongoDAO:
    config = json.load(
        open(relative(__file__, "config/mongoconfig.json")),
    )
    return MongoDAO(
        host=config["host"],
        port=config["port"],
        db_name=config["dbName"],
    )


def main():
    global router
    dao = create_dao()
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
            "<building_name>": Router({
                "fountains": ListFountainsRoute(context),
            }),
        }),
        "campuses": Router({
            "": ListCampusesRoute(context),
            "<campus_name>": Router({
                "buildings": ListBuildingsRoute(context),
            })
        }),
        "fountains": Router({
            "<fountain_name>": Router({
                "ratings": RatingsRoute(context),
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


if __name__ == "__main__":
    main()
