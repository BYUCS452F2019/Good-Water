import shlex
import textwrap
import traceback
from typing import Dict, List

from communicator import Communicator
from commands.get_rating import GetRatingCommand
from commands.handler import CommandHandler
from commands.list_buildings import ListBuildingsCommand
from commands.list_fountains import ListFountainsCommand
from commands.new_user import NewUserCommand
from commands.rate_fountain import RateFountainCommand
from context import ClientContext


class Shell:
    """Manages user interaction with the client."""
    done: bool
    context: ClientContext
    handlers: Dict[str, CommandHandler]

    def __init__(self, host: str, port: int):
        self.done = False
        self.handlers = {}
        self.context = ClientContext(
            communicator=Communicator(host=host, port=port),
        )
        self._register_handlers()

    def _register_handlers(self):
        handler_list: List[CommandHandler] = [
            GetRatingCommand(self.context),
            ListBuildingsCommand(self.context),
            ListFountainsCommand(self.context),
            NewUserCommand(self.context),
            RateFountainCommand(self.context),
        ]

        for handler in handler_list:
            handler.context = self.context
            self.handlers[handler.command_name.lower()] = handler

    def display_help(self):
        print("Good-Water client supports the following commands:")

        msgs = [(n, h.help_text) for n, h in self.handlers.items()]
        msgs += [
            ("help", "Displays this help message."),
            ("exit", "Terminates the client."),
        ]
        msgs.sort()

        for name, help_text in msgs:
            print(name)
            text = textwrap.dedent(help_text).strip()
            help_text = "\n".join(
                "\n".join(textwrap.wrap(
                    text=t,
                    width=100,
                    initial_indent=" " * 4,
                )) for t in text.splitlines()
            )
            print(help_text)

    def read_command(self, cmd: str):
        cmd = cmd.strip()

        if cmd == "":
            return

        args = shlex.split(cmd)
        cmd_name = args[0].lower()

        if cmd_name == "exit":
            self.done = True
        elif cmd_name == "help":
            self.display_help()
        else:
            if cmd_name in self.handlers:
                handler = self.handlers[cmd_name]
                try:
                    handler.run(args)
                except Exception as ex:
                    print(
                        f"{type(ex).__name__} raised"
                        f" during '{cmd_name}' command."
                    )
                    traceback.print_exc()
            else:
                print(f"Unknown command: {cmd_name}")

    def loop(self):
        """Handle user input until the program ends."""
        print("Welcome to the Good-Water client!")
        print("Type 'help' for usage information.")

        while not self.done:
            self.read_command(input("> "))
