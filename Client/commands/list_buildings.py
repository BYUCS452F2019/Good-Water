from typing import List

from commands.handler import CommandHandler
from context import ClientContext


class ListBuildingsCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "listbuildings"
        self.help_text = """
            Usage: 'listbuildings'
            Displays all available buildings.
        """

    def run(self, argv: List[str]):
        if len(argv) != 1:
            print(f"{self.command_name} should have 0 arguments.")
            return

        status, data = self.context.communicator.send_request(
            path="/buildings",
            method="GET",
        )

        if 200 <= status < 300:
            # TODO: properly format buildings
            print(data)
        else:
            print("Failed to retrieve buildings.")
