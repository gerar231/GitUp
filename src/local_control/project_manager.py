import os
from git import Repo
from git import IndexFile
from src.github_control import user_account as uc

class ProjectManager(object):

    def __init__(self, user: uc.UserAccount):
        """
        Construct a new ProjectManager instance to view projects, must be associated with 
        a UserAccount
        """
        self.curr_user = user
        return None

    def view_project_repo(self, path: str):
        """
        Arguments:
            path: the absolute path of the directory to be checked, error if path is invalid.
        
        If the absolute path is an existing working tree directory or a subdirectory then
        GitUp recognizes this as a project and ensures a remote repository is associated
        with the user's account to backup the local repository. If the given path is not 
        part of an existing repository then a new repository is created and associated with
        a remote repository on the user's account. Always returns a Repo instance associated
        with the path.
        """
        # repo_name = os.path.basename(os.path.normpath(local_repo.working_tree_dir))

        # check if valid path, if not then error

        # check if directory is associated with an existing repository
            # if so then get the existing repository and ensure a remote repository is associated
            # with the user's account.
        
            # if the directory is not part of an existing repository then create a new one associated with
            # a remote on the user's GitHub account.
        
        # return the Repo object for this path
        NotImplementedError()
    
    def find_project_repo(self, path: str) -> bool: 
        """
        Arguments:
            path: the absolute path of the directory to be checked.
        
        Returns Repo object if the directory given from path is a working tree directory for 
        a repository or a subdirectory of a working tree, returns None otherwise. 
        """
        NotImplementedError()