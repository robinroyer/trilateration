from __future__ import absolute_import

import unittest

import time
import datetime
from ..utils.tools import is_number
# do not forget to use nose2 at root to run test

 
class Test_utils(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST

    def test_is_number(self):
        self.assertTrue(is_number(.8))

    def test_is_not_number(self):
        self.assertFalse(is_number("coucou"))

    def test_is_not_number2(self):
        self.assertFalse(is_number(2j))

if __name__ == '__main__':
    unittest.main()