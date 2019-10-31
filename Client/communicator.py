import json
from http.client import HTTPConnection
from typing import NamedTuple, Optional, Tuple


class Credentials(NamedTuple):
    username: str
    password: str


AUTH_PATH = "/login"


class Communicator:
    """Sends requests to an HTTP server."""
    host: str
    port: int
    creds: Optional[Credentials]
    token: Optional[str]

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.creds = None
        self.token = None

    def authenticate(self) -> bool:
        """
        Requests a new auth token.
        Returns True iff the authentication was successful.
        """
        if self.creds is None:
            return False

        status, data = self.send_request(
            path=AUTH_PATH,
            method="POST",
            data={
                "username": self.creds.username,
                "password": self.creds.password,
            },
            retry_auth=False,
        )

        if not 200 <= status < 300:
            return False

        self.token = data["token"]
        return True

    def send_request(
            self,
            path: str,
            method: str,
            data: Optional[dict] = None,
            retry_auth=True,
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

            if res.status == 401 and retry_auth:
                # try to get a new token:

                if self._authenticate():
                    return self.send_request(
                        path=path,
                        method=method,
                        data=data,
                        retry_auth=False,
                    )

            return res.status, json.loads(response_data)
        finally:
            conn.close()
