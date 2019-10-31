from typing import Any, Dict, List

from commands.handler import CommandHandler
from context import ClientContext


class RateFountainCommand(CommandHandler):
    def __init__(self, context: ClientContext):
        self.context = context
        self.command_name = "ratefountain"
        self.help_text = """
            Usage: 'ratefountain FOUNTAIN RATING'
            Adds a rating to the given fountain.
        """

    def run(self, argv: List[str]):
        if len(argv) != 3:
            print(f"{self.command_name} should have 2 arguments.")
            return

        fountain_id = argv[1]
        value = float(argv[2])

        status, data = self.context.communicator.send_request(
            path=f"/fountains/{fountain_id}/ratings",
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
            print(f"Failed to rate fountain: {data['error']}.")
