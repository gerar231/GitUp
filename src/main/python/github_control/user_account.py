import os, sys
import github
from github import Github
import git
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
        if os.path.exists("/tmp/gitup") is False:
            os.mkdir("/tmp/gitup")
        default_token_path = os.path.normpath("/tmp/gitup/token.txt")

        # user account fields start as None
        self.__github_control = None
        self.__token = None
        self.__login = None

        # check if a token_path is provided
        if token_path is None:
            token_path = default_token_path 
        else:
            norm_path = os.path.normpath(token_path)
            if os.path.exists(norm_path) is False and user_name is None and password is None:
                sys.stderr.write("Provided token_path {} for login is not a valid file path, using default path {}.\n".format(token_path, default_token_path))
                token_path = default_token_path

        # if any username/password provided
        if user_name and password:
            self.__github_control = Github(login_or_token=user_name, password=password)
            try:
                self.__login = self.__github_control.get_user().login
            except github.GithubException:
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
            with open(token_path, "w+") as token_file:
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
                except (github.GithubException):
                    sys.stderr.write("Provided token_path {} has invalid token, using default path {}.\n".format(token_path, default_token_path))
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
                    except github.GithubException:
                        raise ValueError("Token at default path {} was invalid (might need login refresh).".format(token_path))
            except FileNotFoundError:
                raise ValueError("No user_name and/or password and no token at default path {}.".format(token_path))


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

    def create_remote_repo(self, local_repo: Repo, create_new_origin=False, use_existing_repo=False):
        """
        Arguments:
            local_repo: GitPython Repo object to create a remote repository on the user account.
            create_new_origin: If True then attempts to create a new remote repository under
            existing origin, default is False.
            use_existing_repo: If True then if an existing repo is found on the user's account a
            remote will be created from the local to the existing remote. If no existing remote repo
            is found then a new remote repo will be created.

        Create a remote repository under the name of the parent directory containing the repo
        on the current user's GitHub account and add remote under the name "origin" to this local repository. 
        If an "origin" remote already exists and create_new_origin is False then throw AssertionError.
        If no "origin" remote exists and create_new_origin is True then throw AssertionError.
        If a remote repo with conflicting name exists and use_existing_repo is False then thrown an AssertionError.
        """
        # verify that there is not an origin remote
        try:
            local_repo.remote(name="origin")
            # local repo has origin remote
            if not create_new_origin:
                raise AssertionError("local_repo already has an origin remote and create_new_origin is False.")
        except ValueError:
            # local repo does not have origin remote
            if create_new_origin:
                raise AssertionError("create_remote_repo called with create_new_origin True but no existing origin.")
            pass

        # attempt to create a new remote repository using the folder containing the repository name
        repo_name = os.path.basename(os.path.normpath(os.path.join(local_repo.common_dir, "..")))
        existing_repos = self.get_remote_repos()
        # check if the user has an existing remote repository of this name
        remote_url = None
        for curr_repo in existing_repos:
            if curr_repo[0] == repo_name:
                if not use_existing_repo:
                    raise AssertionError("Existing remote repo found with the name {} and use_existing_repo is False.".format(repo_name))
                else:
                    # if a remote repo is found with a matching name then use the existing one.
                    remote_url = curr_repo[1]
                    break

        # create a new remote repository
        if remote_url is None:
            remote_repo = self.__github_control.get_user().create_repo(name=repo_name, description=str("Repository created by GitUp."))
            print("New remote repository created for {} at {} under the name {}.".format(self.get_login, remote_repo.git_url, repo_name))
            remote_url = str(remote_repo.clone_url)

        # ERROR CHECK NEEDED
        # add the remote from the remote repository to the local repository
        if create_new_origin:
            try:
                local_repo.delete_remote(local_repo.remote())
            except:
                raise git.exc.GitCommandError("Deleting \"origin\" remote failed during create_remote_repo with create_new_origin True.", status=1)

        local_repo.create_remote(name="origin", url=remote_url)
    
    def __create_remote_url(self, local_repo: Repo, remote_name: str):
        """
        Arguments:
            local_repo: Repo the push operation is being performed on.
            remote_name: name of remote associated with Repo local_repo.
        
        Returns a string in the form https://token@remote_repo_url.git for the
        remote_name specified as a remote of local_repo using the GitUp access token and
        the current user's id.
        """
        # get the "origin" remote url, assumes url is the only one and is the first from iterator
        url = next(local_repo.remote(name=remote_name).urls)
        # right half of remote
        url = url.split("https://")
        # splice the url correctly
        url = "https://{}@{}".format(self.__token, url[1])
        return url
    
    def create_clone_url(self, repo_url: str):
        """
        Arguments:
           repo_url: the clone url of the repo to clone in the form https://remote_repo_url.git
        
        Takes in a repo_url of the above form. Returns a repo url in the form 
        https://user_token@remote_repo_url.git to perform a authenticated clone of the remote repo.
        """
        # right half of remote
        url = repo_url.split("https://")
        # splice the url correctly
        url = "https://{}@{}".format(self.__token, url[1])
        return url

    def push_to_remote(self, local_repo):
        """
        Argument:
           local_repo: GitPython repo to push to changes to origin remote.
        
        Pushes the latest changes to the remote repository under remote "origin" to branch master.
        If local_repo does not have a remote named "origin" throw a GitCommandError.
        If push to remote "origin" fails throw GitCommandError.
        """
        # verify this repo has an origin remote
        try:
            local_repo.remote(name="origin")
        except ValueError:
            raise git.exc.GitCommandError("No origin remote for repo {}.".format(local_repo.working_tree_dir), status=1)
        # push to the remote
        try:
            local_repo.git.push(self.__create_remote_url(local_repo, "origin"), "master")
        except:
            raise git.exc.GitCommandError("Push to origin remote failed for repo {}.".format(local_repo.working_tree_dir), status=1)

    def pull_to_local(self, local_repo: Repo):
        """
        Argument:
            local_repo: GitPython repo to pull latest changes from the origin remote
        Pulls the latest changes to this local repository from the remote "origin" on branch master.
        If local_repo does not have a remote named "origin" throw a GitCommandError.
        If pull from remote "origin" fails throw a GitCommandError.
        """
        try:
            local_repo.remote(name="origin")
        except ValueError:
            raise git.exc.GitCommandError("No origin remote for repo {}.".format(local_repo.working_tree_dir), status=1)
        # push to the remote
        try:
            local_repo.git.pull(self.__create_remote_url(local_repo, "origin"), "master")
        except:
            raise git.exc.GitCommandError("Pull to repo {} from remote origin failed.".format(local_repo.working_tree_dir), status=1)