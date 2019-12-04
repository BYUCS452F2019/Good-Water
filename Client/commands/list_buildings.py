from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


def print_buildings(data: List[Dict[str, Any]]):
    for building in data:
        name = building["name"]
        lat = building["latitude"]
        lon = building["longitude"]
        ns = "N" if lat >= 0 else "S"
        ew = "E" if lon >= 0 else "W"
        print(f"name: {name}")
        print(f"{abs(lat)}\u00b0{ns} {abs(lon)}\u00b0{ew}")
        print()


class ListBuildingsCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "listbuildings"
        self.help_text = """
            Usage: 'listbuildings CAMPUSNAME'
            Displays all available buildings.
        """

    def run(self, argv: List[str]):
        if len(argv) != 2:
            print(f"{self.command_name} should have 1 argument.")
            return

        campus_name = argv[1]

        status, data = self.context.communicator.send_request(
            path=f"/campuses/{campus_name}/buildings",
            method="GET",
        )

        if 200 <= status < 300:
            print_buildings(data["buildings"])
        else:
            print(f"Failed to retrieve buildings: {data['error']}")
