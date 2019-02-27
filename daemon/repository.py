import os
import sys
import git
import time
from git.exc import GitCommandError
from datetime import datetime

class RepositoryInitError(Exception):
    pass

# Represents a single repository that GitUp is tracking.
class Repository(git.Repo):
    def __init__(self, path=None, odbt=git.GitCmdObjectDB,
                 search_parent_directories=False, expand_vars=True,
                 dirty="0"):
        try:
            super().__init__(path, odbt, search_parent_directories, expand_vars)
            self.dirty = dirty == "1"
            self.path = os.path.normpath(path)
        except:
            raise RepositoryInitError()

    # Returns True if the given path is containd in this repository, False
    # otherwise.
    def contains(self, path):
        normed_path = os.path.normpath(path)
        prefix = os.path.commonprefix([self.path, normed_path])
        return prefix == self.path

    # Returns the list of changed files for this repo.
    def __get_changed_files(self): 
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
        changed_files = self.__get_changed_files()
        if filepath == None:
            # add and commit all the changes
            for path in changed_files:
                try:
                    self.__add_commit(path)
                    self.dirty = True
                except GitCmdError:
                    print(("{}: Committing failed.\n\trepo: {}"
                            + "\n\tfile: {}").format(self.__get_timestamp(),
                            self.path, path), file=sys.stderr)
        elif filepath in changed_files or filepath in self.untracked_files:
            try:
                self.__add_commit(filepath)
                self.dirty = True
            except:
                print(("{}: Committing failed.\n\trepo: {}"
                        + "\n\tfile: {}").format(self.__get_timestamp(),
                        self.path, filepath), file=sys.stderr)

    def __get_timestamp(self): 
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S')
 
    # Called when an event occurs in the repository.
    def handle_event(self, event):
        (_, type_names, path, filename) = event
        # Print to the log.
        print("{}: event recieved\n\trepository: {}\n\tpath: {}" + 
                "\n\t filename: {}\n\tevent_types: [{}]".format(
                self.__get_timestamp(), self.path, path, filename, type_names))
        # Commit the changes.
        last_dir = os.path.abspath(os.path.curdir)
        os.chdir(self.path)
        relative_path = os.path.relpath(os.path.join(path, filename))
        self.__safe_commit(filepath=relative_path)
        os.chdir(last_dir)

    # Called when the daemon is first started.
    def on_daemon_start(self):
        # Commit any changes that may have occured while the daemon was down.
        changed_files = self.__get_changed_files()
        if len(changed_files) != 0:
            print("{}: encountered uncommited changes.\n\trepo: {}\n\tfiles [{}]"
                  .format(self.__get_timestamp(), self.path, changed_files))
        # Commit any changes that somehow got missed since the last daemon run.
        self.__safe_commit()

    # Pulls the remote for this repository. Returns True on success, False on
    # failure.
    def safe_pull(self):
        try:
            self.git.pull("GitUp", "master")
            return True
        except GitCommandError:
            print("{}: failed to pull remote.\n\trepo: {}".format(
                    self.__get_timestamp(), self.path), file=sys.stderr)
            return False

    # Pushes to the remote for this repository. Returns True on success, False
    # on failure
    def safe_push(self):
        try:
            self.git.push("GitUp", "master")
            self.dirty = False
            return True
        except GitCommandError:
            print("{}: failed to push to remote.\n\trepo: {}".format(
                     self.__get_timestamp(), self.path), file=sys.stderr)
            return False
        

