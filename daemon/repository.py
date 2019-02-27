import os
import sys
import git
import time
from datetime import datetime

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

    # Returns True if the given path is containd in this repository, False
    # otherwise.
    def contains(self, path):
        normed_path = os.path.normpath(path)
        prefix = os.path.commonprefix([self.path, normed_path])
        return prefix == self.path

    def __get_chaged_files(self): 
        return [ os.path.normpath(item.a_path) 
                 for item in self.index.diff(None) ]

    # Add and commit the given filepath. If a message is provided it will be
    # used as the commit message otherwise the filepath will be used as the
    # commit message. 
    def __add_commit(self, filepath, message=None):
        if message == None:
            message = filepath
        self.git.add(filepath)
        self.git.commit(filepath, m=message)

    # Add and commit the given filepath, or all unstaged changes if no filepath
    # is given, If the provided file doesn't have unstaged changes does nothing.
    def __safe_commit(self, filepath=None):
        changed_files = self.get_changed_files()
        if filepath == None:
            # add and commit all the changes
            for path in changed_files:
                self.__add_commit(path)
        elif filepath in changed_files or filepath in self.untracked_files:
            self.__add_commit(filepath)

    def handle_event(self, event):
        (_, type_names, path, filename) = event 
        print("REPOSITORY=[{}] PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              self.path, path, filename, type_names))
        last_dir = os.path.abspath(os.path.curdir)
        os.chdir(self.path)
        relative_path = os.path.relpath(os.path.join(path, filename))
        self.__safe_commit(filepath=relative_path)
        os.chdir(last_dir)

    def on_daemon_start(self):
        changed_files = self.get_changed_files()
        if len(changed_files) != 0:
            ts = time.time()
            current_time = datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S')
            print("TIME [{}]: encountered uncommited changes: FILES [{}]"
                  .format(current_time, changed_files))
        # Commit any changes that somehow got missed since the last daemon run.
        self.__safe_commit()

