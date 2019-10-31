from typing import List

from commands.handler import CommandHandler
from context import ClientContext


class NewUserCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "newuser"
        self.help_text = """
            Usage: 'newuser email password'
            Creates a new user account.
        """

    def run(self, argv: List[str]):
        if len(argv) != 3:
            print(f"{self.command_name} should have 2 arguments.")
            return

        email, password = argv[1:3]
        status, data = self.context.communicator.send_request(
            path="/users",
            method="POST",
            data={
                "email": email,
                "password": password,
            },
        )

        if 200 <= status < 300:
            print("User successfully created.")
        else:
            print("User creation failed.")
