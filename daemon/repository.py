import os
import git

class RepositoryInitError(Exception):
    pass

# Represents a single repository that GitUp is tracking.
class Repository(git.Repo):
    def __init__(self, path=None, odbt=git.GitCmdObjectDB,
                 search_parent_directories=False, expand_vars=True,
                 last_pulled=None):
        try:
            super().__init__(path, odbt, search_parent_directories, expand_vars)
            self.last_pulled = last_pulled
            self.path = os.path.normpath(path)
        except:
            raise RepositoryInitError()

    def contains(self, path):
        normed_path = os.path.normpath(path)
        prefix = os.path.commonprefix([self.path, normed_path])
        return prefix == self.path

    def handle_event(self, event):
        (_, type_names, path, filename) = event 
        print("REPOSITORY=[{}] PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              self.path, path, filename, type_names))
