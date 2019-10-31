import http.server
import json
import socketserver

from routes.router import Router
from routes.list_buildings import ListBuildingsRoute
from routes.list_fountains import ListFountainsRoute

PORT = 8080

ROUTER = Router({
    "buildings": Router({
        "": ListBuildingsRoute(),
        "<building_name>": Router({
            "fountains": ListFountainsRoute(),
        }),
    })
})


class Handler(http.server.SimpleHTTPRequestHandler):
    def _handle(self, method):
        content_len = self.headers.get("Content-Length", failobj=0)

        if content_len == 0:
            body = None
        else:
            body = json.loads(self.rfile.read(content_len))

        status, response = ROUTER.handle(
            path=self.path.split("/", 1)[-1],
            method=method,
            body=body,
            params={},
        )

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

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)

        httpd.serve_forever()

        # This class is responsible for making API endpoints that
        # will receive JSON objects and then call DAO methods such as "addUser"
        # "addBuildling" etc.


if __name__ == "__main__":
    main()
