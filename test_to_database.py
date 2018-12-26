import unittest
from to_database import DatabaseWriter

writer = DatabaseWriter()


class test_make_connection(unittest.TestCase):
    def test_make_connection(self):
        self.assertRaises(ArithmeticError,
                          writer.make_connection())
