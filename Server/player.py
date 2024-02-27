from uuid import UUID

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        display_name (str): The name displayed for the player.
        color (int): The color of the player.
        uuid (str): The unique identifier of the player.
        ready (bool): Whether the player is ready to start the game.
    """
    def __init__(self, display_name: str, color: int, uuid: str, ready:bool = False):
        self.uuid: UUID = UUID(uuid)
        self.display_name = display_name
        self.color = color
        self.ready = ready

    def __dict__(self) -> dict:
        return {
            "display_name": self.display_name,
            "color": self.color,
            "uuid": str(self.uuid),
            "ready": self.ready
        }
    
    @classmethod
    def from_dict(cls, player_dict: dict):
        return cls(player_dict["display_name"], player_dict["color"], player_dict["uuid"], player_dict["ready"])