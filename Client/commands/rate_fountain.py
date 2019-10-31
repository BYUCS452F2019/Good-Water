from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


class RateFountainCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "ratefountain"
        self.help_text = """
            Usage: 'ratefountain BUILDING FOUNTAIN RATING'
            Adds a rating to the given fountain.
        """

    def run(self, argv: List[str]):
        if len(argv) != 4:
            print(f"{self.command_name} should have 3 arguments.")
            return

        building_name = argv[1]
        fountain_id = argv[2]
        value = float(argv[3])

        status, data = self.context.communicator.send_request(
            path=f"/buildings/{building_name}/fountains/{fountain_id}/ratings",
            method="POST",
            data={
                "rating": {
                    "value": value,
                },
            },
        )

        if 200 <= status < 300:
            print("Fountain rated.")
        else:
            print(f"Failed to rate fountains: {data['error']}.")
