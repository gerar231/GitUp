import os

# Represents a single repository that GitUp is tracking
class Repository(object):
    def __init__(self, remote, local_path, last_pulled):
        self.remote = remote
        self.local_path = os.path.normpath(local_path)
        self.last_pulled = last_pulled

    def contains(self, path):
        normed_path = os.path.normpath(path)
        prefix = os.path.commonprefix([self.local_path, normed_path])
        return prefix == self.local_path

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

    def handle_event(self, event):
        (_, type_names, path, filename) = event 
        print("REPOSITORY=[{}] PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              self.local_path, path, filename, type_names))
