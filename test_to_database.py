import unittest
from to_database import DatabaseWriter


class test_make_connection(unittest.TestCase):
    def test_make_connection(self):
        writer = DatabaseWriter()
        self.assertRaises()
