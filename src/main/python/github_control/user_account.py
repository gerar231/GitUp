import os, sys
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

    def __init__(self, user_name: str=None, password: str=None, token_path: str=None):
        """
        Arguments:
            user_name: user name for a GitHub account, assumes valid if given.
            password: password for a GitHub account, assumes valid if given.
            token_path: opens the file at this path and reads the first line for an authorization token, if provided.

        If no arguments provided:
            Checks default_token_path, if no token exists at the default path then throw a ValueError. 
            If token at default path is invalid then throw a ValueError.

        If user_name or password are provided:
            Uses provided token_path or default_token_path if none, if neither are valid then Value Error. 
            
        If only a token_path is provided:
            Checks the file given at path for an authorization token, if none or invalid path then print error message 
            and check the default path. If no token exists at default path and no username and password then throw error.

        If user_name and password are provided:
            Logs in to a user account and creates a new token for GitUp that
            will be stored with the scopes of "user, delete_repo, repo" at the the provided path or 
            default_token_path if not provided.
            If a token for GitUp already exists at the used path then remove the existing
            token and write the new token.
            If user_name and password are invalid then throw a ValueError.
        """
        # TODO: refresh Oauth token
        # TODO: handle deleting tokens when a user logs out or just different behavior for passing in a new username and password

        # file path used to store a GitHub Access token.
        default_token_path = os.path.normpath(os.path.join(os.path.realpath(__file__), "token.txt"))

        # check if a token_path is provided
        if token_path is None:
            token_path = default_token_path 
        else:
            norm_path = os.path.normpath(token_path)
            if os.path.exists(norm_path) is False and user_name is None and password is None:
                sys.stderr.write("Provided token_path for login is not a valid file path, using default path {}".format(token_path))
                token_path = default_token_path

        # if any username/password provided
        if user_name and password:
            self.__github_control = Github(login_or_token=user_name, password=password)
            try:
                self.__login = self.__github_control.get_user().login
            except GithubException.BadCredentialsException:
                raise ValueError("Invalid user_name and/or password provided.")
            # get existing authorizations if for GitUp then delete, then create new auth token.
            authorizations = self.__github_control.get_user().get_authorizations()
            for auth in authorizations:
                if auth.note_url == "https://github.com/gerar231/GitUp":
                    auth.delete()
            # create a new token
            token = self.__github_control.get_user().create_authorization(scopes=["user", "delete_repo", "repo"], note_url="https://github.com/gerar231/GitUp", 
                note="GitUp Authorization token.").token
            # write the token at the path
            with open(token_path, "w") as token_file:
                print("New token created for {}: {}.".format(self.__login, token))
                token_file.writelines(token)
            # set token for this session
            self.__token = token
            return
        else:
            # no username or password provided, use token_path.
            existing_token = None
            if token_path != default_token_path:
                # user provided token path that wasn't default
                try:
                    with open(token_path) as token_file:
                        existing_token = token_file.readline()
                        self.__github_control = Github(login_or_token=existing_token)
                        self.__login = self.__github_control.get_user().login
                        self.__token = existing_token
                        # provided token is valid, exit the method.
                        return
                except (FileNotFoundError, GithubException.BadCredentialsException):
                    sys.stderr.write("Provided token_path for login is not a valid file path, using default path {}".format(token_path))
                    token_path = default_token_path
            # checking default_token_path
            try:
                with open(token_path) as token_file:
                    existing_token = token_file.readline() 
                    self.__github_control = Github(login_or_token=existing_token)
                    try:
                        self.__login = self.__github_control.get_user().login
                        self.__token = existing_token
                        # token at default path is valid, exit the method
                        return
                    except GithubException.BadCredentialsException:
                        raise ValueError("Token at default path {} was invalid (might need login refresh).".format(token_path))
            except FileNotFoundError:
                raise ValueError("No user_name and/or password and no token at default path {1}.".format(token_path))


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
        If a remote repo with conflicting name exist then thrown an AssertionError.
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
            for curr_repo in existing_repos:
                if curr_repo.name == repo_name:
                    raise AssertionError("Existing remote repo found with the name {}.".format(repo_name))

            # create a new remote repository
            remote_repo = self.__github_control.get_user().create_repo(name=repo_name, description=str("Repository managed by GitUp."))
            print(remote_repo.git_url)

            # ERROR CHECK NEEDED
            # add the remote from the remote repository to the local repository
            remote_url = str(remote_repo.clone_url)
            local_repo.create_remote(name="GitUp", url=remote_url)
            
            # add all changes
            local_repo.git.add(".")

            # commit 
            local_repo.git.commit(m="GitUp added all changes after creating remote repo.")

            # push to the remote using https://token@remote_url.git
            # perform a push using the git binary, specifying the url dynamically generated in the above format
            if local_repo.git.push(self.__create_remote_url(local_repo, "GitUp"), "master") is None:
                raise exc.GitCommandError("Push to origin failed after remote repo created for {}".format(os.path.join(local_repo.common_dir, "..")))
    
    def __create_remote_url(self, local_repo: Repo, remote_name: str):
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
        
        Pushes the latest changes to the remote repository under remote "GitUp" to branch master.
        If local_repo does not have a remote named "GitUp" throw a GitCommandError.
        If push to remote "GitUp" fails throw GitCommandError.
        """
        # verify this repo has a GitUp remote
        try:
            local_repo.remote(name="GitUp")
        except ValueError:
            raise exc.GitCommandError("No GitUp remote for repo {}.".format(local_repo.working_tree_dir))
        # push to the remote
        if local_repo.git.push(self.__create_remote_url(local_repo, "GitUp"), "master") is None:
            raise exc.GitCommandError("Push to GitUp remote failed for repo {}.".format(local_repo.working_tree_dir))

    def pull_to_local(self, local_repo: Repo):
        """
        Argument:
            local_repo: GitPython repo to pull latest changes from the GitUp remote
        Pulls the latest changes to this local repository from the remote "GitUp" on branch master.
        If local_repo does not have a remote named "GitUp" throw a GitCommandError.
        If pull from remote "GitUp" fails throw a GitCommandError.
        """
        try:
            local_repo.remote(name="GitUp")
        except ValueError:
            raise exc.GitCommandError("No GitUp remote for repo {}.".format(local_repo.working_tree_dir))
        # push to the remote
        if local_repo.git.pull(self.__create_remote_url(local_repo, "GitUp"), "master") is None:
            raise exc.GitCommandError("Pull to repo {} from remote GitUp failed.".format(local_repo.working_tree_dir))
