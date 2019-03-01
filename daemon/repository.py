import os
import sys
import git
import time
from datetime import datetime
from git.exc import GitCommandError
sys.path.append(os.path.normpath("../src/main/python/gui/"))
from github_control.user_account import UserAccount

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

    # Prints an error message about failure to commit the given file.
    def __commit_failure(self, path):
        print(("{}: Committing failed.\n\trepo: {}\n\tfile: {}").format(
                self.__get_timestamp(), self.path, path), file=sys.stderr)

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
                    self.__commit_failure(path)
        elif filepath in changed_files or filepath in self.untracked_files:
            try:
                self.__add_commit(filepath)
                self.dirty = True
            except:
                self.__commit_failure(filepath)

    # Returns a formated string representing the current time.
    def __get_timestamp(self): 
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S')
 
    # Called when an event occurs in the repository.
    def handle_event(self, event, user_account):
        (_, type_names, path, filename) = event
        # Print to the log.
        print(("{}: event received.\n\trepository: {}\n\tpath: {}" + 
                "\n\tfilename: {}\n\tevent_types: {}").format(
                self.__get_timestamp(), self.path, path, filename, type_names))
        # Commit the changes.
        last_dir = os.path.abspath(os.path.curdir)
        os.chdir(self.path)
        relative_path = os.path.relpath(os.path.join(path, filename))
        self.__safe_commit(filepath=relative_path)
        os.chdir(last_dir)

    # Called when the daemon is first started.
    def on_daemon_start(self, user_account):
        # Pull first.
        self.safe_pull(user_account)
        # Commit any changes that may have occured while the daemon was down.
        changed_files = self.__get_changed_files()
        if len(changed_files) != 0:
            print("{}: encountered uncommited changes.\n\trepo: {}\n\tfiles [{}]"
                  .format(self.__get_timestamp(), self.path, changed_files))
        # Commit any changes that somehow got missed since the last daemon run.
        self.__safe_commit()
        # Push last.
        self.safe_push(user_account)

    # Print an error message about failing to pull the remote.
    def __pull_failure(self):
        print("{}: failed to pull remote.\n\trepo: {}".format(
                self.__get_timestamp(), self.path), file=sys.stderr)

    # Pulls the remote for this repository. Returns True on success, False on
    # failure.
    def safe_pull(self, user_account):
        print("{}: pulling.\n\trepo: {}".format(
                self.__get_timestamp(), self.path))
        if not user_account:
            self.__pull_failure()
            return False
        try:
            user_account.pull_to_local(self)
            return True
        except GitCommandError:
            self.__pull_failure()
            return False
   
    # Print an error message about failing to push to the remote. 
    def __push_failure(self):
        print("{}: failed to push to remote.\n\trepo: {}".format(
                self.__get_timestamp(), self.path), file=sys.stderr)

    # Pushes to the remote for this repository. Returns True on success, False
    # on failure
    def safe_push(self, user_account):
        print("{}: pushing.\n\trepo: {}".format(
                self.__get_timestamp(), self.path))
        if not user_account:
            self.__push_failure()
            return False
        try:
            user_account.push_to_remote(self)
            self.dirty = False
            return True
        except GitCommandError:
            self.__push_failure()
            return False
        

