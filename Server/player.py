import uuid

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, display_name: str, color: int, uuid: str = None):
        if uuid:
            self._uuid: uuid.UUID = uuid.UUID(id)
        else:
            self._uuid: uuid.UUID = uuid.uuid4()
        self.display_name = display_name
        self.color = color

    @property
    def uuid(self):
        return self._uuid