from statistics import Statistics
import uuid

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        self._uuid: uuid.UUID = uuid.uuid4()
        self._id: int =  self._uuid.int
        self.display_name = display_name
        self.statistics = statistics

class RemotePlayer(Player):
    """
    Represents a remote player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        super().__init__(id, display_name, statistics)

class LocalPlayer(Player):
    """
    Represents a local player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        super().__init__(id, display_name, statistics)

class ComputerPlayer(Player):
    """
    Represents a computer player in the game.
    
    Attributes:
        _id (int): The unique identifier of the player.
        display_name (str): The name displayed for the player.
        statistics (Statistics): The statistics of the player.
    """
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        super().__init__(id, display_name, statistics)
