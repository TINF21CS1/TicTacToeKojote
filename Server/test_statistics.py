import unittest
from Server.statistics import Statistics


class TestStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.abspath("Server/Data/test_statistics.db")
        cls.statistics = Statistics(path=path)
    def setUp(self):
        statistics = Statistics(path = "./data/test_statistics.json")
        statistics.delete_all_statistics()
    def test_add_profile(self):
        statistics = Statistics()
        statistics.delete_all_statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 0, 3, 0, 0, 0, 0, 0, 0))
        self.assertEqual(statistics.get_all_statistics(), [("test", 0, 3, 0, 0, 0, 0, 0, 0)])
        statistics.add_profile("test2", draws_first=1, loses_second= 2)
        self.assertEqual(statistics.get_statistics("test2"),
                         ("test2", 0, 0, 0, 2, 1, 0, 0, 0))
        self.assertEqual(statistics.get_all_statistics(),
                         [("test", 0, 3, 0, 0, 0, 0, 0, 0), ("test2", 0, 0, 0, 2, 1, 0, 0, 0)])
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_update_statistics(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        statistics.update_statistics("test", "wins_first", 2)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 1, 3, 0, 0, 0, 0, 2, 0))
        statistics.update_statistics("test", "wins_second", 4)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 1, 4, 0, 0, 0, 0, 6, 0))
        statistics.update_statistics("test", "draws_first", 1)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 1, 4, 0, 0, 1, 0, 7, 0))
        statistics.update_statistics("test", "draws_second", 5)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 1, 4, 0, 0, 1, 1, 12, 0))
        statistics.update_statistics("test", "loses_first", 2)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 1, 4, 1, 0, 1, 1, 14, 0))
        statistics.update_statistics("test", "loses_second", 3)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 1, 4, 1, 1, 1, 1, 17, 0))
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_get_statistics(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        self.assertEqual(statistics.get_statistics("test"),
                         ("test", 0, 3, 0, 0, 0, 0, 0, 0))
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_get_all_statistics(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        statistics.add_profile("test2", draws_first=1, loses_second= 2)
        self.assertEqual(statistics.get_all_statistics(),
                         [("test", 0, 3, 0, 0, 0, 0, 0, 0), ("test2", 0, 0, 0, 2, 1, 0, 0, 0)])
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_delete_all_statistics(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_delete_statistics(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        statistics.add_profile("test2", draws_first=1, loses_second= 2)
        (statistics.delete_statistics("test"))
        self.assertEqual(statistics.get_all_statistics(), [("test2", 0, 0, 0, 2, 1, 0, 0, 0)])
        statistics.delete_statistics("test2")
        self.assertEqual(statistics.get_all_statistics(), [])
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_count_emojis(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=0, wins_second= 3)
        statistics.count_emojis("test", "🤔 🙈 me así, se 😌 ds 💕👭👙 hello 👩🏾‍🎓 emoji hello 👨‍👩‍👦‍👦 how are 😊 you today🙅🏽🙅🏽")
        self.assertEqual(statistics.get_statistics("test"), ("test", 0, 3, 0, 0, 0, 0, 0, 11))
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])


    def test_get_wins(self):
        statistics = Statistics()
        statistics.add_profile("test", wins_first=1, wins_second= 3)
        self.assertEqual(statistics.get_wins("test"), 4)
        self.assertEqual(statistics.get_wins("test", type="first"), 1)
        self.assertEqual(statistics.get_wins("test", type = "second"), 3)
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_get_loses(self):
        statistics = Statistics()
        statistics.add_profile("test", loses_first=1, loses_second= 3)
        self.assertEqual(statistics.get_loses("test"), 4)
        self.assertEqual(statistics.get_loses("test", type="first"), 1)
        self.assertEqual(statistics.get_loses("test", type = "second"), 3)
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_get_draws(self):
        statistics = Statistics()
        statistics.add_profile("test", draws_first=1, draws_second= 3)
        self.assertEqual(statistics.get_draws("test"), 4)
        self.assertEqual(statistics.get_draws("test", type="first"), 1)
        self.assertEqual(statistics.get_draws("test", type = "second"), 3)
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_get_emojis(self):
        statistics = Statistics()
        statistics.add_profile("test", emojis=11)
        self.assertEqual(statistics.get_emojis("test"), 11)
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])

    def test_get_moves(self):
        statistics = Statistics()
        statistics.add_profile("test", moves=11)
        self.assertEqual(statistics.get_moves("test"), 11)
        statistics.delete_all_statistics()
        self.assertEqual(statistics.get_all_statistics(), [])


    def test_errors(self):
        statistics = Statistics()
        with self.assertRaises(ValueError):
            statistics.get_statistics("test")
        with self.assertRaises(ValueError):
            statistics.get_moves("test")
        with self.assertRaises(ValueError):
            statistics.get_emojis("test")
        with self.assertRaises(ValueError):
            statistics.get_draws("test")
        with self.assertRaises(ValueError):
            statistics.get_loses("test")
        with self.assertRaises(ValueError):
            statistics.get_wins("test")



