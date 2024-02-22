import uuid

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, id: int, display_name: str, color: int):
        self._uuid: uuid.UUID = uuid.uuid4()
        self._id: int =  self._uuid.int
        self.display_name = display_name
        self.color = color
