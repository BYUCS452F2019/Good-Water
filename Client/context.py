from communicator import Communicator


class ClientContext:
    """Manages the state of the client application."""
    communicator: Communicator

    def __init__(
            self,
            communicator: Communicator,
    ):
        self.communicator = communicator
