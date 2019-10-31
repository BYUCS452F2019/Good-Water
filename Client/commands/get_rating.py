from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


class GetRatingCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "getrating"
        self.help_text = """
            Usage: 'getrating BUILDING FOUNTAIN'
            Gets the average rating for a fountain.
        """

    def run(self, argv: List[str]):
        if len(argv) != 3:
            print(f"{self.command_name} should have 2 arguments.")
            return

        building_name = argv[1]
        fountain_id = argv[2]

        status, data = self.context.communicator.send_request(
            path=f"/buildings/{building_name}/fountains/{fountain_id}/ratings",
            method="GET",
        )

        if 200 <= status < 300:
            value = data["averageValue"]
            print(f"Average rating: {value}")
        else:
            print(f"Failed to retrieve ratings: {data['error']}.")
