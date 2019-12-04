from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


def print_campuses(data: List[Dict[str, Any]]):
    for campus in data:
        name = campus["name"]
        city = campus["city"]
        state = campus["state"]
        print(f"name: {name}")
        print(f"location: {city}, {state}")
        print()


class ListCampusesCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "listcampuses"
        self.help_text = """
            Usage: 'listcampuses'
            Displays all available campuses.
        """

    def run(self, argv: List[str]):
        if len(argv) != 1:
            print(f"{self.command_name} should have 0 arguments.")
            return

        status, data = self.context.communicator.send_request(
            path=f"/campuses",
            method="GET",
        )

        if 200 <= status < 300:
            print_campuses(data["campuses"])
        else:
            print(f"Failed to retrieve campuses: {data['error']}")
