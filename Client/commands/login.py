from typing import List

from commands.handler import CommandHandler
from communicator import Credentials
from context import ClientContext


class LoginCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "login"
        self.help_text = """
            Usage: 'login USERNAME PASSWORD'
            Signs the user in.
        """

    def run(self, argv: List[str]):
        if len(argv) != 3:
            print(f"{self.command_name} should have 2 arguments.")
            return

        username, password = argv[1:3]
        self.context.communicator.creds = Credentials(username, password)

        if self.context.communicator.authenticate():
            print("User signed in.")
        else:
            print("User failed to sign in.")
