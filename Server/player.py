from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        uuid (UUID): The UUID of the player.
        display_name (str): The display name of the player.
        color (int): The color of the player.
        color_str (str): The color of the player as a html string.
        ready (bool): Whether the player is ready to start the game.

    Class Methods:
        from_dict(player_dict: dict) -> Player: Create a Player object from a dictionary.
        with_color_str(display_name: str, color_str: str, uuid: UUID = None, ready: bool = False) -> Player: Create a Player object with an html string as color instead of an int.
    """
    def __init__(self, display_name: str, color: int, uuid: UUID = None, ready:bool = False):
        self.uuid: UUID = uuid if uuid else uuid4()
        self.display_name = display_name
        self.color = color
        self.ready = ready

    def as_dict(self) -> dict:
        return {
            "display_name": self.display_name,
            "color": self.color,
            "uuid": str(self.uuid),
            "ready": self.ready
        }
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return str(self.uuid) == str(other.uuid)
    
    def __hash__(self) -> int:
        return hash(self.uuid)
    
    @classmethod
    def from_dict(cls, player_dict: dict):
        return cls(player_dict["display_name"], player_dict["color"], UUID(player_dict["uuid"]), player_dict["ready"])
    
    @classmethod
    def with_color_str(cls, display_name: str, color_str: str, uuid: UUID = None, ready:bool = False):
        return cls(display_name, int(color_str[1:], 16), uuid, ready)
    
    @property
    def color_str(self) -> str:
        return f"#{self.color:06x}"

    @color_str.setter
    def color_str(self, color: str):
        self.color = int(color.removeprefix('#'), 16)