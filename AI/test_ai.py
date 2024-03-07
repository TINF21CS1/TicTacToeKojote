import unittest
from . import ai_strategy

# write unittest that tests the get_empty_cells method of the AI class
class TestAIStrategy(ai_strategy.AIStrategy):

    def __init__(self):
        pass

    def do_turn(self):
        pass
        

class TestAI(unittest.TestCase):
    
    def test_get_empty_cells1(self):
        ai = TestAIStrategy()
        game_status = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
    
    # Write different testcases for every possible gamestatus
    def test_get_empty_cells2(self):
        ai = TestAIStrategy()
        game_status = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
        
    def test_get_empty_cells3(self):
        ai = TestAIStrategy()
        game_status = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
        
    def test_get_empty_cells4(self):
        ai = TestAIStrategy()
        game_status = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        self.assertEqual(ai.get_empty_cells(game_status), [])

    def test_get_empty_cells5(self):
        ai = TestAIStrategy()
        game_status = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)])
        
    def test_get_empty_cells6(self):
        ai = TestAIStrategy()
        game_status = [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)])
        
    def test_get_empty_cells7(self):
        ai = TestAIStrategy()
        game_status = [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)])
    
    # now create testcases where the second and first player have made some moves
    def test_get_empty_cells8(self):
        ai = TestAIStrategy()
        game_status = [[1, 0, 0], [0, 0, 0], [0, 0, 2]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 1), (0, 2), (1,0), (1, 1), (1, 2), (2, 0), (2, 1)])
        
    def test_get_empty_cells9(self):
        ai = TestAIStrategy()
        game_status = [[1, 0, 0], [0, 0, 0], [0, 1, 2]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 1), (0, 2), (1,0),(1, 1), (1, 2), (2, 0)])
        
    def test_get_empty_cells10(self):
        ai = TestAIStrategy()
        game_status = [[1, 0, 0], [2, 1, 2], [0, 1, 2]]
        self.assertEqual(ai.get_empty_cells(
            game_status), [(0, 1), (0, 2), (2, 0)])
        

if __name__ == "__main__":
    unittest.main()