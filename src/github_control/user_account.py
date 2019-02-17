from github import Github

class UserAccount(object):
    """
    This class manages information about the currently logged in user 
    for interacting with the UI and Daemon.
    """

    def __init__(self, user_name, password):
        """
        Logs in to a user account and intializes the object
        """
        self.github_control = Github(login_or_token=user_name, password=password)
    
    def get_name(self):
        """
        Returns the user name for the current user
        """
        return self.github_control.get_user()._name
    
    def get_profile_url(self):
        """
        Returns the profile URL for the current user
        """
        return self.github_control.get_user()._url

    def github_controller(self):
        """
        Returns the GitHub controller for this user (allows pushing & pulling from Repository)
        """
        return self.github_control