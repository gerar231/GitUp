import os
from git import Repo
from git import IndexFile
from src.github_control import user_account as uc

class LocalRepoManager(object):

    def __init__(self):
        """
        Construct a new LocalRepoManager instance to load and create local GitRepositories, optionally
        associated with a UserAccount.
        """
        return None

    def create_repo(self, name: str, path: str, user: uc.UserAccount=None):
        """
        Arguments:
            name: the name of the desired working_tree_directory (top-level) 
            path: the relative path to create the desired working_tree_directory
            user: UserAccount to associate this repository with, optional.
        
        Creates a new Git Repository, throws error if invalid path. If a UserAccount object
        is passed in with the method then it creates a remote repository associated with this
        local repository on the UserAccount.
        """
        #repo_name = os.path.basename(os.path.normpath(local_repo.working_tree_dir))
        return None
    
    def load_repo(self, path: str, user: uc.UserAccount=None):
        """
        Arguments:
            path: the relative path to load the repository.
            user: UserAccount to associate this repository with, optional.
        
        Loads an existing Git Repository, throws error if invalid path or invalid repository. 
        If a UserAccount object is passed in with the method then it creates a remote 
        repository associated with this local repository on the UserAccount.
        """
        #repo_name = os.path.basename(os.path.normpath(local_repo.working_tree_dir))
        return None