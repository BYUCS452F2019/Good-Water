import json
from http.client import HTTPConnection
from typing import Optional, Tuple


class Communicator:
    """Sends requests to an HTTP server."""
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_request(
            self,
            path: str,
            method: str,
            data: Optional[dict] = None,
    ) -> Tuple[int, dict]:
        """
        Sends an HTTP request.

        Parameters
        ----------
        - path:
            The path of the request URL relative to the host.
        - method:
            The HTTP method of the request.
        - data (optional):
            The body of the HTTP request.

        Returns
        -------
        A tuple of HTTP status number and response body.
        """
        try:
            conn = HTTPConnection(
                host=self.host,
                port=self.port,
            )
            params = {}

            if data is not None:
                params["body"] = json.dumps(data)

            conn.request(method, path, **params)
            res = conn.getresponse()
            response_data = res.read()
            return res.status, json.loads(response_data)
        finally:
            conn.close()
