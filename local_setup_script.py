from local_control import project_manager as pm
from github_control import user_account as uc
user = uc.UserAccount()
project = pm.ProjectManager(user)
import os
path = os.path.normpath(os.path.join(os.getcwd(), ".."))
path
path2 = os.path.normpath(os.path.join(path, "..", "..", "..", "test-repo"))