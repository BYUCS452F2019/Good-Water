from typing import List

from commands.handler import CommandHandler
from communicator import Credentials
from context import ClientContext


class NewUserCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "newuser"
        self.help_text = """
            Usage: 'newuser USERNAME PASSWORD'
            Creates a new user account.
        """

    def run(self, argv: List[str]):
        if len(argv) != 3:
            print(f"{self.command_name} should have 2 arguments.")
            return

        username, password = argv[1:3]
        status, data = self.context.communicator.send_request(
            path="/users",
            method="POST",
            data={
                "username": username,
                "password": password,
            },
        )

        if not 200 <= status < 300:
            print("User creation failed.")
            return

        print("User successfully created. Signing in...")
        self.context.communicator.creds = Credentials(username, password)

        if self.context.communicator.authenticate():
            print("User signed in.")
        else:
            print("User failed to sign in.")
