import os
import shutil
import re
import sys
import git
import time
from datetime import datetime
from git.exc import GitCommandError
sys.path.append(os.path.normpath("../"))
from github_control.user_account import UserAccount

# Represents a single repository that GitUp is tracking.
class Repository(git.Repo):
    def __init__(self, path=None, odbt=git.GitCmdObjectDB,
                 search_parent_directories=False, expand_vars=True,
                 dirty="0"):
        super().__init__(path, odbt, search_parent_directories, expand_vars)
        self.dirty = dirty == "1"
        self.path = os.path.normpath(path)

    # Returns True if the given path is containd in this repository, False
    # otherwise.
    def contains(self, path):
        normed_path = os.path.normpath(path)
        prefix = os.path.commonprefix([self.path, normed_path])
        return prefix == self.path

    # Returns the list of changed files for this repo.
    def __get_changed_files(self): 
        return [ os.path.normpath(item.a_path) 
                 for item in self.index.diff(None) ] + self.untracked_files

    # return a commit message for the given filepath based on the chnages that have
    # been made to it.
    def __get_commit_message(self, filepath, is_del):
        if is_del:
            return "delete " + filepath
        elif filepath in self.__get_changed_files():
            # unified=0 is important so every hunk starts at the modified line,
            # this makes the hunk headers accurate.
            try:
                diff = self.git.diff("HEAD", filepath, unified=0)
            except GitCommandError as e:
                print("{}: failed to diff file {}.".format(self.__get_timestamp(), filepath),
                      file=sys.stderr)
                print(e, file=sys.stderr)
                return filepath
            message = ""
            for line in diff.splitlines():
                regex = re.compile("^@@.+@@")
                if regex.match(line):
                   print(line)
                   # chop the header and following space out of the line.
                   line = line[line.find("@@", line.find("@@") + 1) + 3:]
                   if line not in message:
                       message += line + "\n"
            if message:
                return filepath + ": " + message
        return filepath

    # Add and commit the given filepath. If a message is provided it will be
    # used as the commit message otherwise the result of self.__get_commit_message(filepath)
    # will be used as the commit message. 
    def __add_commit(self, filepath, is_del, message=None):
        if message == None:
            message = self.__get_commit_message(filepath, is_del)
        self.git.add(filepath)
        self.git.commit(filepath, m=message)

    # Prints an error message about failure to commit the given file.
    def __commit_failure(self, path):
        print(("{}: Committing failed.\n\trepo: {}\n\tfile: {}").format(
                self.__get_timestamp(), self.path, path), file=sys.stderr)

    # Add and commit the given filepath, or all unstaged changes if no filepath
    # is given, If the provided file doesn't have unstaged changes does nothing.
    def __safe_commit(self, filepath=None, is_dir=False, is_del=False):
        changed_files = self.__get_changed_files()
        if filepath == None:
            # add and commit all the changes
            for path in changed_files:
                try:
                    self.__add_commit(path, is_del)
                    self.dirty = True
                except GitCommandError as e:
                    self.__commit_failure(path)
                    print(e, file=sys.stderr)
        # Directories don't show up in the untracked files so we have to
        # manually check if this is a directory
        elif is_dir or filepath in changed_files:
            try:
                self.__add_commit(filepath, is_del)
                self.dirty = True
            except GitCommandError as e:
                self.__commit_failure(filepath) 
                print(e, file=sys.stderr)

    # Returns a formated string representing the current time.
    def __get_timestamp(self): 
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S')
 
    # Called when an event occurs in the repository.
    def handle_event(self, event, user_account):
        (_, type_names, path, filename) = event
        is_dir = False
        # Print to the log.
        print(("{}: event received.\n\trepository: {}\n\tpath: {}" + 
                "\n\tfilename: {}\n\tevent_types: {}").format(
                self.__get_timestamp(), self.path, path, filename, type_names))
        # Commit the changes.
        last_dir = os.path.abspath(os.path.curdir)
        os.chdir(self.path)
        relative_path = os.path.relpath(os.path.join(path, filename))
        if "IN_ISDIR" in type_names:
            is_dir = True
            # add a separator to the end of the path.
            relative_path += os.sep
        is_del = "IN_DELETE" in type_names or "IN_DELETE_SELF" in type_names
        self.__safe_commit(filepath=relative_path, is_dir=is_dir, is_del=is_del)
        os.chdir(last_dir)

    # create the git attributes file for the given repository if one does not exist.
    def __create_git_attributes(self):
        filepath = os.path.join(self.path, ".gitattributes")
        if not os.path.exists(filepath):
            print("{}: creating new .gitattributes\n\trepo: {}"
                    .format(self.__get_timestamp(), self.path))
            try:
                print(os.path.abspath(os.path.curdir), file=sys.stderr)
                shutil.copy(os.path.relpath("git_attributes.txt"), filepath)
            except Exception as e:
                print("{}: failed to setup .gitattributes\n\trepo: {}"
                        .format(self.__get_timestamp(), self.path), file=sys.stderr)
                print(e, file=sys.stderr)
        else:
            print("{}: found existing .gitattributes\n\trepo: {}"
                    .format(self.__get_timestamp(), self.path))

    # Called when the daemon is first started.
    def on_daemon_start(self, user_account):
        # Pull first.
        self.safe_pull(user_account)
        self.__create_git_attributes() 
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

    def __contains_merge(self):
        merge_head_path = os.path.join(self.git_dir, "MERGE_HEAD")
        return os.path.exists(merge_head_path) 

    # Pulls the remote for this repository. Returns True on success, False on
    # failure.
    def safe_pull(self, user_account):
        print("{}: pulling.\n\trepo: {}".format(
                self.__get_timestamp(), self.path))
        if self.__contains_merge():
           print("{}: already in merge not pulling.\n\trepo: {}".format(
                   self.__get_timestamp(), self.path))
           return False
        if not user_account:
            self.__pull_failure()
            print("\n\tno user account", file=sys.stderr)
            return False
        try:
            user_account.pull_to_local(self)
            return True
        except GitCommandError as e:
            self.__pull_failure()
            print(e, file=sys.stderr)
            if self.__contains_merge():
                print("{}: encountered merge conflict.\n\trepo: {}".format(
                    self.__get_timestamp(), self.path))
                # TODO display an error message to the user.
                self.__safe_commit()
                try:
                    user_account.set_upstream_push_to_remote(self)
                except GitCommandError as err:
                    print("{}: failed to push merge conflict.\n\trepo: {}".format(
                            self.__get_timestamp(), self.path), file=sys.stderr)
                    print(err, file=sys.stderr)
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
            print("\n\tno user account.", file=sys.stderr)
            return False
        try:
            user_account.push_to_remote(self)
            self.dirty = False
            return True
        except GitCommandError as e:
            self.__push_failure()
            print(e, file=sys.stderr)
            return False

