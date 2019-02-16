from py_daemon.py_daemon import Daemon
from inotify.adapters import InotifyTrees
import os.path
import csv

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


# Parses the repository information stored in the given repo_file and returns
# a list  of repository objects correspoding to the data in the file.
def parse_repositories(repo_file_path):
    with open(repo_file_path) as repo_file:
        repositories = []
        csv_reader = csv.reader(repo_file, delimiter=',')
        line = 0
        for row in csv_reader:
            if line != 0:
                remote = row[0]
                local_path = row[1]
                last_pulled = row[2]
                repo = Repository(remote, local_path, last_pulled)
                repositories.append(repo)
            line += 1
        return repositories

# Allows this process to be turned into a Daemon
class GitUpDaemon(Daemon):
    def __init__(self, pidfile, stdin=os.devnull,
                 stdout=os.devnull, stderr=os.devnull,
                 home_dir='.', umask=0o22, verbose=1,
                 use_gevent=False, repofile=None):
        super(GitUpDaemon, self).__init__(pidfile, stdin, stdout, stderr, home_dir,
                                          umask, verbose, use_gevent)
        self.repofile = repofile

    def run(self):
        if self.repofile:      
            self.repositories = parse_repositories(self.repofile)
            local_paths = list(map(lambda x: x.local_path, self.repositories))
            inotify = InotifyTrees(local_paths)
            for event in inotify.event_gen(yield_nones=False):
                self.handle_event(event)
        else:
            print "No repofile provided stopping self"
            self.stop()
   
    # Handle the given inotify event
    def handle_event(self, event):
        for repo in self.repositories:
             event_path = event[2]
             if repo.contains(event_path):
                 repo.handle_event(event)

