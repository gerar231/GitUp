# Put unit tests here for UserAccount using Python's unittest module: https://docs.python.org/3/library/unittest.html
import unittest, sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..")))
from user_account import UserAccount

class TestUserAccount(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    # insert more tests here
    def test_construct(self):
        project = UserAccount()
        self.assertEqual(True, True)
        self.assertTrue(True)
        self.assertRaises(ValueError)

    def tearDown(self):
        return super().tearDown()