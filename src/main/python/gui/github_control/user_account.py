import os
from github import Github
from github import GithubException
from git import Repo
from git import IndexFile
from git import exc
import typing

class UserAccount(object):
    """
    This class manages information about the currently logged in user (and their remote repositories)
    for interacting with the UI and Daemon.
    """

    def __init__(self, user_name: str=None, password: str=None, token_file_path: str=None):
        """
        Arguments:
            user_name: user name for a GitHub account, assumes valid if given.
            password: password for a GitHub account, assumes valid if given.
            token_file_path: opens the file at this path and reads the first line for an authorization token, if provided.
        If a token_file_path is provided:
            Checks the file given at path for an authorization token, if none or invalid path then throw ValueError. 
            If a token exists and is invalid then throw a ValueError.
        If user_name and password are provided:
            Logs in to a user account and creates a token for GitUp that
            will be stored with the scopes of "user, delete_repo, repo" at the path /tmp/GitUp/token.txt.
            If a token for GitUp already exists at the path /tmp/GitUp/token.txt then login to that user.
        
        If no arguments provided:
            searches default path /tmp/GitUp/token.txt for token, if no token exists then throw ValueError.
        
        In all cases, if this user does not have a public key associated with this 
        """
        # TODO: refresh Oauth token
        # TODO: handle deleting tokens when a user logs out or just different behavior for passing in a new username and password
        if token_file_path:
            norm_path = os.path.normpath(token_file_path)
            if os.path.exists(norm_path) is False:
                raise ValueError("token_file_path is not a valid file path.")
        else:
            token_file_path = os.path.normpath("token.txt")
            if os.path.exists(token_file_path) is None and user_name is None and password is None:
                raise ValueError("No token file at default path {1}".format(token_file_path))

        # check for an existing token
        existing_token = None
        try:
            with open(token_file_path) as token_file:
                existing_token = token_file.readline() 
        except FileNotFoundError:
            existing_token = None

        if existing_token:
            if user_name and password:
                print(ValueError("A user token already exists, cannot login to a new user."))
            self.__github_control = Github(login_or_token=existing_token)
            try:
                self.__login = self.__github_control.get_user().login
            except GithubException.BadCredentialsException:
                raise(ValueError("Invalid token provided in first line of file at {1}".format(token_file_path)))
            # set token for this session
            self.__token = existing_token
            return

        if user_name and password:
            self.__github_control = Github(login_or_token=user_name, password=password)
            try:
                self.__login = self.__github_control.get_user().login
            except GithubException.BadCredentialsException:
                raise(ValueError("Invalid user_name and/or password provided."))
            # get existing authorizations if for GitUp then delete, then create new auth token.
            authorizations = self.__github_control.get_user().get_authorizations()
            for auth in authorizations:
                if auth.note_url == "https://github.com/gerar231/GitUp":
                    auth.delete()
            # create a new token
            token = self.__github_control.get_user().create_authorization(scopes=["user", "delete_repo", "repo"], note_url="https://github.com/gerar231/GitUp", 
                note="GitUp Authorization token.").token
            # write the token at the default path
            with open(token_file_path, "w") as token_file:
                print(token)
                token_file.writelines(token)
            # set token for this session
            self.__token = token

    def get_name(self):
        """
        Returns the name associated with this user account.
        """
        return self.__github_control.get_user().name
    
    def get_login(self):
        """
        Returns the user (screen) login associated with this user account.
        """
        return self.__login
    
    def get_profile_url(self):
        """
        Returns the profile URL for the current user
        """
        return self.__github_control.get_user().html_url

    def get_profile_image_url(self):
        """
        Returns the profile image URL for the current user
        """
        return self.__github_control.get_user().avatar_url
    
    def get_remote_repos(self):
        """
        Returns a list of tuples in the form: 
        (repo_name, repo_clone_url)
        representing the name's and clone urls of the current user's remote repositories.
        """
        repos = list()
        for repo in self.__github_control.get_user().get_repos():
            repos.append(tuple([repo.name, repo.clone_url]))
        return repos

    def create_remote_repo(self, local_repo: Repo):
        """
        Arguments:
            local_repo: GitPython Repo object to create a remote repository on the user account.
        Create a remote repository under the name of the parent directory containing the repo
        on the current user's GitHub account and add remote under the name "GitUp" to this local repository. 
        Adds all changes and pushes all contents of local repo into remote repo after creation.
        If a "GitUp" remote already exists throw an AssertionError.
        If a remote repo with conflicting name exists then new remote repo created with name + (number of conflicts)
        If push fails after a remote repo is created then throw a GitCommandError.
        """
        # verify that there is not a GitUp remote
        try:
            local_repo.remote(name="GitUp")
            raise AssertionError("local_repo already has a GitUp remote.")
        except ValueError:
            # attempt to create a new remote repository using the folder containing the repository name
            repo_name = os.path.basename(os.path.normpath(os.path.join(local_repo.common_dir, "..")))
            existing_repos = self.__github_control.get_user().get_repos()
            # check if the user has an existing remote repository of this name
            i = 0
            for curr_repo in existing_repos:
                if curr_repo.name == repo_name:
                    i = i + 1
                    repo_name = repo_name + str(i)
                    # raise AssertionError("Existing remote repo found with the name {}.".format(repo_name))

            # create a new remote repository
            remote_repo = self.__github_control.get_user().create_repo(name=repo_name, description=str("Repository managed by GitUp."))
            print(remote_repo.git_url)

            # ERROR CHECK NEEDED
            # add the remote from the remote repository to the local repository
            remote_url = str(remote_repo.html_url + ".git")
            local_repo.create_remote(name="GitUp", url=remote_url)
            
            # add all changes
            local_repo.git.add(".")

            # commit 
            local_repo.git.commit(m="GitUp added all changes after creating remote repo.")

            # push to the remote using https://token@remote_url.git
            # perform a push using the git binary, specifying the url dynamically generated in the above format
            if local_repo.git.push(self.__create_push_url(local_repo, "GitUp"), "master") is None:
                raise exc.GitCommandError("Push to origin failed after remote repo created for {}".format(os.path.join(local_repo.common_dir, "..")))
    
    def __create_push_url(self, local_repo: Repo, remote_name: str):
        """
        Arguments:
            local_repo: Repo the push operation is being performed on.
            remote_name: name of remote associated with Repo local_repo.
        
        Returns a string in the form https://user_login:token@remote_repo_url.git for the
        remote_name specified as a remote of local_repo using the GitUp access token and
        the current user's id.
        """
        # get the "GitUp" remote url, assumes url is the only one and is the first from iterator
        url = next(local_repo.remote(name=remote_name).urls)
        # right half of remote
        url = url.split("https://")
        # splice the url correctly
        url = "https://{}@{}".format(self.__token, url[1])
        return url
    
    def push_to_remote(self, local_repo):
        """
        Argument:
           local_repo: GitPython repo to push to changes to GitUp remote.
        
        Pushes the latest changes to the remote repository under remote "GitUp".
        If local_repo does not have a remote named "GitUp" throw a GitCommandError.
        If push to remote "GitUp" fails throw GitCommandError.
        """
        # verify this repo has a GitUp remote
        try:
            local_repo.remote(name="GitUp")
        except ValueError:
            raise exc.GitCommandError("No GitUp remote for repo {}.".format(local_repo.working_tree_dir))
        # push to the remote
        if local_repo.git.push(self.__create_push_url(local_repo, "GitUp"), "master") is None:
            raise exc.GitCommandError("Push to GitUp remote failed for repo {}.".format(local_repo.working_tree_dir))

    def pull_to_local(self, local_repo: Repo):
        """
        Argument:
            local_repo: GitPython repo to pull latest changes from the GitUp remote
        Pulls the latest changes to this local repository from the remote "GitUp".
        If local_repo does not have a remote named "GitUp" throw a GitCommandError.
        If pull from remote "GitUp" fails throw a GitCommandError.
        """
        try:
            local_repo.remote(name="GitUp")
        except ValueError:
            raise exc.GitCommandError("No GitUp remote for repo {}.".format(local_repo.working_tree_dir))
        # push to the remote
        if local_repo.remote(name="GitUp").pull() is None:
            raise exc.GitCommandError("Pull to repo {} from remote GitUp failed.".format(local_repo.working_tree_dir))
