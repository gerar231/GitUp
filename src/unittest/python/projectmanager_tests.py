# Put tests for ProjectManager here using using Python's unittest module: https://docs.python.org/3/library/unittest.html
import unittest, sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..")))
from project_manager import ProjectManager

class TestProjectManager(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    # insert more tests here
    def test_construct(self):
        project = ProjectManager()
        self.assertEqual(True, True)
        self.assertTrue(True)
        self.assertRaises(ValueError)

    def tearDown(self):
        return super().tearDown()