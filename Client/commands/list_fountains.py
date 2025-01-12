from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


def print_fountains(data: List[Dict[str, Any]]):
    for fountain in data:
        fountain_name = fountain["name"]
        print(f"name: {fountain_name}")


class ListFountainsCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "listfountains"
        self.help_text = """
            Usage: 'listfountains BUILDINGNAME'
            Displays all available fountains in the given building.
        """

    def run(self, argv: List[str]):
        if len(argv) != 2:
            print(f"{self.command_name} should have 1 argument.")
            return

        building_name = argv[1]

        status, data = self.context.communicator.send_request(
            path=f"/buildings/{building_name}/fountains",
            method="GET",
        )

        if 200 <= status < 300:
            print_fountains(data["fountains"])
        else:
            print(f"Failed to retrieve fountains: {data['error']}.")
