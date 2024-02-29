from . import ai_strategy
from threading import Thread

class AIContext():

    def __init__(self, strategy: ai_strategy.AIStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ai_strategy.AIStrategy):
        self._strategy = strategy

    # Runs the strategy as a new thread and returns the thread
    def run_strategy(self):
        thread = Thread(target=self._strategy.run)
        thread.start()
        return thread
