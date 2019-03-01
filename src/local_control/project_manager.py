import os
import git
from git import Repo
from git import IndexFile
from github_control import user_account as uc

class ProjectManager(object):

    def __init__(self, user: uc.UserAccount):
        """
        Construct a new ProjectManager instance to view projects, must be associated with 
        a UserAccount
        """
        self.curr_user = user
        return None

    def find_project_repo(self, path: str) -> Repo: 
        """
        Arguments:
            path: the absolute path of the directory to be checked.
        
        Returns Repo object if the directory given from path is a working tree directory for 
        a repository or a subdirectory of a working tree, returns None otherwise. 
        """
        norm_path = os.path.normpath(path)
        if os.path.exists(norm_path) is False:
            raise ValueError("Path given to find a repository is not a valid file path.")
        else:
            try:
                return Repo(path, search_parent_directories=True)
            except:
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
        norm_path = os.path.normpath(path)
        if os.path.exists(norm_path) is False:
            raise ValueError("Path given to view a project is not a valid file path.")

        # check if directory is associated with an existing repository
        repo = self.find_project_repo(norm_path)

        if repo is None:
            # if the directory is not part of an existing repository then create a new one associated with
            # a remote on the user's GitHub account.
            # CREATE A NEW REPOSITORY
            repo = Repo.init(path=norm_path, bare=True)
        # ensure the repository has the GitUp remote
        if not repo.remote(name="GitUp").exists:
            self.curr_user.create_remote_repo(repo)
        # return the Repo object for this path
        return repo    

    def restore_project_repo(self, path: str, repo_name: str):
        """
        Arguments:
            path: the absolute path of the directory to restore the repository, error if path is invalid.
            repo_name: the name of the repository as shown on GitHub, error if the current user does not
                have a repo associated with this name.

        Restores the latest version of a project on a remote repository (associated with the user's GitHub
        account) to a folder created using the repo_name at the given path. Returns the repository object if 
        restored properly, otherwise returns None.
        """
        norm_path = os.path.normpath(path)
        if os.path.exists(norm_path) is False:
            raise ValueError("Path given to restore a project is not a valid file path.")

        # check if the directory is associated with an existing repository
        repo = self.find_project_repo(norm_path)

        if not repo is None:
            raise ValueError("Path provided to an existing project.")

        # check if the repo_name exsits on the users account
        existing_repos = self.curr_user.get_remote_repos()
        found_repo = None
        for r in existing_repos:
            if r[0] == repo_name:
                found_repo = r

        # clone the repo to the path
        if found_repo is None:
            raise ValueError("No existing project repository with repo_name for this user's account.")
        
        # join norm path with repo_name for new directory
        norm_path = os.path.join(norm_path, repo_name)

        return git.Repo.clone_from(found_repo[1], norm_path, branch='master')
    
    def delete_project_repo(self, path: str, remove_files=False):
        """
        Arguments:
            path: the absolute path of a working tree directory of an existing local repository, error if no repo.
            remove_files: if True remove the repository files on the user's GitHub acccount.
        
        Removes the GitUp remote from a local repository. Deletes the repository files on the users
        GitHub account if remove_files is True. Returns True if repository successfully removed,
        returns False if the repository was not removed.
        """
        # check if the path is valid
            # if the path is not valid then throw an error
        # check if the directory is associated with an existing repository
            # if the directory is not associated with an existing repository then throw an error
        # get the name of the repository
        # remove the GitUp remote from the local repository
        # check that the repository name exists on the user's GitHub account
        # if remove_files is True then remove_files from GitHub
        raise NotImplementedError()