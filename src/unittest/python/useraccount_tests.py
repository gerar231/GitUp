# Put unit tests here for UserAccount using Python's unittest module: https://docs.python.org/3/library/unittest.html
import unittest, sys, os
sys.path.append(os.path.normpath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "main", "python")))
from github_control.user_account import UserAccount

class TestUserAccountInit(unittest.TestCase):
    
    def setUp(self):
        return super().setUp()

    def test_no_arguments(self):
        print("TestUserAccountInit test_no_arguments.")

    def test_only_token_path_invalid(self):
        print("TestUserAccountInit test_only_token_path_invalid.")

    def test_only_token_path_valid(self):
        print("TestUserAccountInit test_only_token_path_valid.")

    def test_user_name_or_password(self):
        print("TestUserAccountInit test_user_name_or_password.")

    def test_user_name_and_password_invalid(self):
        print("TestUserAccountInit test_user_name_and_password_invalid.")

    def test_user_name_and_password_valid(self):
        print("TestUserAccountInit test_user_name_and_password_valid.")

    def test_user_name_and_password_invalid_with_path(self):
        print("TestUserAccountInit test_user_name_and_password_invalid_with_path.")

    def test_user_name_and_password_valid_with_path(self):
        print("TestUserAccountInit test_user_name_and_password_valid_with_path.")

    def tearDown(self):
        return super().tearDown()

class TestUserAccountInformation(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def test_get_name(self):
        print("TestUserAccountInformation test_get_name.")

    def test_get_login(self):
        print("TestUserAccountInformation test_get_login.")
        
    def test_get_profile_url(self):
        print("TestUserAccountInformation test_get_profile_url.")

    def test_get_profile_image_url(self):
        print("TestUserAccountInformation test_get_profile_image_url.")

    def test_get_remote_repos(self):
        print("TestUserAccountInformation test_get_remote_repos.")

    def tearDown(self):
        return super().tearDown()

class TestUserAccountCreateRemoteRepo(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def test_existing_origin(self):
        print("TestUserAccountCreateRemoteRepo test_existing_origin.")

    def test_existing_remote_repo_name(self):
        print("TestUserAccountCreateRemoteRepo test_existing_remote_repo_name.")

    def test_push_failure(self):
        print("TestUserAccountCreateRemoteRepo test_push_failure.")

    def test_valid_creation(self):
        print("TestUserAccountCreateRemoteRepo test_valid_creation.")

    def tearDown(self):
        return super().tearDown()

class TestUserAccountPushToRemote(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def test_no_origin(self):
        print("TestUserAccountPushToRemote test_no_origin.")

    def test_bad_remote_repo(self):
        print("TestUserAccountPushToRemote test_bad_remote_repo.")

    def test_no_master_branch(self):
        print("TestUserAccountPushToRemote test_no_master_branch.")

    def test_valid_push(self):
        print("TestUserAccountPushToRemote test_valid_push.")

    def tearDown(self):
        return super().tearDown()

class TestUserAccountPullToLocal(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def test_no_origin(self):
        print("TestUserAccountPullToLocal test_no_origin.")

    def test_bad_remote_repo(self):
        print("TestUserAccountPullToLocal test_bad_remote_repo.")

    def test_no_master_branch(self):
        print("TestUserAccountPullToLocal test_no_master_branch.")
    
    def test_valid_pull(self):
        print("TestUserAccountPullToLocal test_valid_pull.")

    def tearDown(self):
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()