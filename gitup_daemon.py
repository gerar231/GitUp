from py_daemon.py_daemon import Daemon
from inotify.adapters import InotifyTree

# The repository information is stored in this file.
REPOSITORY_FILE_PATH = "/usr/GitUp/repositories.csv"

# Represents a single repository that GitUp is tracking
class Repository(object):
    def __init__(self, remote, local_path, last_pulled):
        self.remote = remote
        self.local_path = local_path
        self.last_pulled = last_pulled

    # Returns True if GitUp is capable of connecting to GitHub to
    # push/pull for this repository. False otherwise.
    def connected(self):
        # TODO implement this
        return False

    # Pushes all of the local changes to this repository.
    def push(self):
        # TODO implement this
        return

    # Pull all of the changes from the remote to the local repository.
    # Updates self.last_pulled and the 'repositories.csv' file.
    def pull(self):   
         # TODO implement this
        return
    
    # Commits the changes to the given file to the local repository.
    def commit_file(self, editted_file_path):
        # TODO implement this
        return


# Parses the repository information stored in the given repo_file and returns
# a list  of repository objects correspoding to the data in the file.
def parse_respoitories(repo_file):
    # TODO implement this
    return None
    
# Allows this process to be turned into a Daemon
class GitUpDaemon(Daemon):
    def run(self):
        repositories = parse_repositories(REPOSITORY_FILE_PATH)
        inotify = InotifyTree
        for repo in repositories:
            inotify.add_watch(repo.local_path)

        for event in inotify.event_gen(yield_nones=False):
            self.handle_event(event)
        # TODO Implement this
        return
   
    # Handle the given inotify event
    def handle_event(event):
        # TODO Implement this
        return

