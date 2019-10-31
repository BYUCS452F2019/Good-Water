from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


class GetRatingCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "getrating"
        self.help_text = """
            Usage: 'getrating FOUNTAIN'
            Gets the average rating for a fountain.
        """

    def run(self, argv: List[str]):
        if len(argv) != 2:
            print(f"{self.command_name} should have 1 arguments.")
            return

        fountain_id = argv[1]

        status, data = self.context.communicator.send_request(
            path=f"fountains/{fountain_id}/ratings",
            method="GET",
        )

        if 200 <= status < 300:
            value = data["averageValue"]
            print(f"Average rating: {value}")
        else:
            print(f"Failed to retrieve ratings: {data['error']}.")
