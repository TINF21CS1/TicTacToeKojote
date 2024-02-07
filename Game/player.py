class Player:
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        self._id = id
        self.display_name = display_name
        self.statistics = statistics

class RemotePlayer(Player):
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        super(id, display_name, statistics)

class LocalPlayer(Player):
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        super(id, display_name, statistics)

class ComputerPlayer(Player):
    def __init__(self, id: int, display_name: str, statistics: Statistics):
        super(id, display_name, statistics)
