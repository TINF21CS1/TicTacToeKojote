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
        ready (bool): Whether the player is ready to start the game.
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
    
    @classmethod
    def from_dict(cls, player_dict: dict):
        return cls(player_dict["display_name"], player_dict["color"], UUID(player_dict["uuid"]), player_dict["ready"])