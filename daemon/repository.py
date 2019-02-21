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
        last_dir = os.path.abspath(os.path.curdir)
        os.chdir(self.path)
        relative_path = os.path.relpath(os.path.join(path, filename))
        # Check to avoid commiting files multiple times or if no changes have occured
        changed_files = [ os.path.normpath(item.a_path) 
                          for item in self.index.diff(None) ]
        filepath = os.path.normpath(relative_path)
        if filepath in changed_files or filepath in self.untracked_files:
            self.git.add(relative_path)
            self.git.commit(relative_path, m=relative_path)
        os.chdir(last_dir)
                            

