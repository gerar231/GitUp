# Put tests for ProjectManager here using using Python's unittest module: https://docs.python.org/3/library/unittest.html
import unittest, sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "main", "python")))
from local_control.project_manager import ProjectManager

class TestProjectManagerFindRepo(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def test_bad_path(self):
        print("TestProjectManagerFindRepo test_bad_path.")

    def test_direct_path(self):
        print("TestProjectManagerFindRepo test_direct_path.")

    def test_child_path(self):
        print("TestProjectManagerFindRepo test_child_path.")

    def test_parent_path(self):
        print("TestProjectManagerFindRepo test_parent_path.")

    def tearDown(self):
        return super().tearDown()

class TestProjectManagerViewRepo(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def test_bad_path(self):
        print("TestProjectManagerViewRepo test_bad_path.")

    def test_no_repo_path(self):
        print("TestProjectManagerViewRepo test_no_repo_path.")

    def test_existing_repo_path(self):
        print("TestProjectManagerViewRepo test_existing_repo_path.")

    def tearDown(self):
        return super().tearDown()

class TestProjectManagerRestoreRepo(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def test_bad_path(self):
        print("TestProjectManagerRestoreRepo test_bad_path.")

    def test_existing_path(self):
        print("TestProjectManagerRestoreRepo test_existing_path.")

    def test_bad_repo_name(self):
        print("TestProjectManagerRestoreRepo test_bad_repo_name.")

    def test_valid_restore(self):
        print("TestProjectManagerRestoreRepo test_valid_restore.")

    def test_authenticated_restore(self):
        print("TestProjectManagerRestoreRepo test_authenticated_restore.")

    def tearDown(self):
        return super().tearDown()

@unittest.skip("delete_project_repo is not implemented yet.")
class TestProjectManagerDeleteRepo(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()