from base_daemon import Daemon
from repository import Repository
from repository import RepositoryInitError
from inotify.adapters import InotifyTrees
import inotify
import os
import csv

event_mask = (inotify.constants.IN_CLOSE_WRITE |
              inotify.constants.IN_MOVE |
              inotify.constants.IN_MODIFY |
              inotify.constants.IN_ISDIR |
              inotify.constants.IN_CREATE |
              inotify.constants.IN_DELETE |
              inotify.constants.IN_DELETE_SELF |
              inotify.constants.IN_MOVE_SELF)

# Daemon that monitors file accesses in the repositories specificed in
# the repofile passed to it's constructor.
class GitUpDaemon(Daemon):
    def __init__(self, pidfile, stdin=os.devnull,
                 stdout=os.devnull, stderr=os.devnull,
                 home_dir='.', umask=0o22, verbose=1,
                 use_gevent=False, repofile=None):
        super().__init__(pidfile, stdin, stdout, stderr, home_dir,
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
            paths = list(map(lambda x: x.path, self.repositories))
            inotify = InotifyTrees(paths,mask=event_mask)
            # Notify the repositories that we are now watching them.
            for repo in self.repositories:
                repo.on_daemon_start()
            # Watch events in repositories
            for event in inotify.event_gen(yield_nones=False):
                if self.__should_process_event(event):
                    self.__handle_event(event)
        else:
            # A client might end up in the case if they don't pass a repofile to
            # the constructor. Allowing the user to not pass a repofile, makes
            # it easier for the user to construct the daemon when they only want
            # to stop it.
            print >> self.stderr, ("run() called without providing a repofile")
            self.stop()
  
    # Returns True if the given event should be passed along to a
    # Repository to be processed, False if it should be ignored.
    def __should_process_event(self, event):
        path = event[2]
        # Makes sure the .git directory get's ignored.
        if ".git" in path:
            return False
        filename = event[3]
        # All directory events should be considered.
        if filename == None:
            return True
        return not self.__ignores_file_type(filename)

    # Returns True if the given type of file should be ignored, False
    # otherwise.
    def __ignores_file_type(self, filename):
        # For now we only ignore .swp files automatically.
        return filename.endswith(".swp") or filename.endswith(".swx")

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
                path = row[0]
                last_pulled = row[1]
                try:
                    repo = Repository(path=path, last_pulled=last_pulled)
                    self.repositories.append(repo)
                except RepositoryInitError:
                    print >> self.stderr, ("repository for " + path + "failed to"
                        + " be initialized skipping")
            line += 1

