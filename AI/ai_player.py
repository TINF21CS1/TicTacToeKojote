from . import ai_strategy

class AIContext():

    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy: ai_strategy.AIStrategy):
        self._strategy = strategy