from uuid import UUID, uuid4

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        uuid (UUID): The UUID of the player.
        display_name (str): The display name of the player.
        color (int): The color of the player.
        ready (bool): Whether the player is ready to start the game.
    """
    def __init__(self, display_name: str, color: int, uuid: UUID = uuid4(), ready:bool = False):
        self.uuid: UUID = uuid
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
        return self.uuid == other.uuid
    
    def __hash__(self) -> int:
        return hash(self.uuid)
    
    @classmethod
    def from_dict(cls, player_dict: dict):
        return cls(player_dict["display_name"], player_dict["color"], player_dict["uuid"], player_dict["ready"])