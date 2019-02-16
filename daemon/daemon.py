from py_daemon.py_daemon import Daemon
from repository import Repository
from inotify.adapters import InotifyTrees
import csv

# Daemon that monitors file accesses in the repositories specificed in
# the repofile passed to it's constructor.
class GitUpDaemon(Daemon):
    def __init__(self, pidfile, stdin=os.devnull,
                 stdout=os.devnull, stderr=os.devnull,
                 home_dir='.', umask=0o22, verbose=1,
                 use_gevent=False, repofile=None):
        super(GitUpDaemon, self).__init__(pidfile, stdin, stdout, stderr, home_dir,
                                          umask, verbose, use_gevent)
        self.repofile = repofile
        self.repositories = []

    # Called when the daemon is started or restarted. May be called directly to
    # run the daemon connected to a terminal for easier testing.
    def run(self):
        if self.repofile:
            # Parse repositories on every run to allow restarting to daemon to
            # update the repositories.
            self.__parse_repositories()
            local_paths = list(map(lambda x: x.local_path, self.repositories))
            inotify = InotifyTrees(local_paths)
            for event in inotify.event_gen(yield_nones=False):
                self.__handle_event(event)
        else:
            # A client might end up in the case if they don't pass a repofile to
            # the constructor. Allowing the user to not pass a repofile, makes
            # it easier for the user to construct the daemon when they only want
            # to stop it.
            print >> self.stderr, "run() called without providing a repofile"
            self.stop()
   
    # Handle the given inotify event, finds the repository it pertains to
    # and forwards the event to that repository.
    def __handle_event(self, event):
        for repo in self.repositories:
             event_path = event[2]
             if repo.contains(event_path):
                 repo.handle_event(event)
    
    # Parses the repository information stored in self.repofile, and stores the
    # Repostiory objects in self.repositories.
    def __parse_repositories(self):
        # if the repository file fails to open there is nothing we can do.
        try:
            repo_csv = open(self.repofile, 'r')
        except IOError:
            print >> self.stderr, "failed ot open repofile"
            self.stop()
        csv_reader = csv.reader(repo_csv, delimiter=',')
        line = 0
        for row in csv_reader:
            if line != 0:
                remote = row[0]
                local_path = row[1]
                last_pulled = row[2]
                repo = Repository(remote, local_path, last_pulled)
                self.repositories.append(repo)
            line += 1

