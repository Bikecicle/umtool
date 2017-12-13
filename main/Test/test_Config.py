from __future__ import print_function
import unittest
from Utils.Config import get_str_option

class TestConfigClass(unittest.TestCase):
    def test_create_job(self):
        option = get_str_option("database_port")
        self.assertEqual("27017", option)

if __name__ == '__main__':
    unittest.main()
