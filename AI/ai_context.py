from . import ai_strategy
from threading import Thread
import time

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
        thread = Thread(target=self._strategy.thread_entry, daemon=True)
        thread.start()
        return thread

if __name__ == "__main__":
    weak_ai = ai_strategy.WeakAIStrategy()
    # create ai context
    ai_context = AIContext(weak_ai)
    # run the strategy
    ai_context.run_strategy()
    time.sleep(3)
    # create strong ai strategy: set arg to true to indicate that it is the second AI-player in the game(this is needed if AIs play against each other)
    strong_ai = ai_strategy.AdvancedAIStrategy(True)
    # set the strategy
    strong_context = AIContext(strong_ai)
    # run the strategy
    strong_context.run_strategy()