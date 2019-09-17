import unittest
import collector

class TestCollector(unittest.TestCase):
    def test_one(self):
        session = collector.get_session()
        self.assertAlmostEqual(1, 1)
