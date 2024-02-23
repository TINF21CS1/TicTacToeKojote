from uuid import UUID

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, display_name: str, color: int, uuid: str, ready:bool = False):
        self.uuid: UUID = UUID(uuid)
        self.display_name = display_name
        self.color = color
        self.ready = ready