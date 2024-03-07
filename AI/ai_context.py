from . import ai_strategy
from threading import Thread

class AIContext():

    """
    Use: AIContext(strategy: ai_strategy.AIStrategy)
    -> Pass the strategy(WeakAIStrategy or StrongAIStrategy) to the AIContext, then call run_strategy() to run the strategy as a new thread.
    It will then connect to localhost and play the game using the strategy.
    """

    def __init__(self, strategy: ai_strategy.AIStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ai_strategy.AIStrategy):
        self._strategy = strategy

    # Runs the strategy as a new thread and returns the thread
    def run_strategy(self):
        thread = Thread(target=self.thread_entry)
        thread.start()
        return thread
