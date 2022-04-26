import unittest
from os.path import exists
import os

import main


class MyTestCase(unittest.TestCase):
    def test_create_csv(self):
        self.assertTrue(exists("output.csv"))

    def test_create_dataframe(self):
        self.assertTrue(os.listdir('./data'))

    def test_read_json(self):
        self.assertEqual(main.read_json('test.json'), '{ "name":"John", "age":30, "city":"New York"}')


if __name__ == '__main__':
    unittest.main()
