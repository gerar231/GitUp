import os
import sys
import inotify
import csv
import time
from datetime import datetime
from inotify.adapters import InotifyTrees
from apscheduler.schedulers.background import BackgroundScheduler
from .base_daemon import Daemon
from .repository import Repository
sys.path.append(os.path.normpath("../"))
from github_control.user_account import UserAccount

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
        self.scheduler = BackgroundScheduler()
        self.push_pull_job = None
        self.user_account = None

    # Push and pull every repository.
    def __push_pull(self):
        for repo in self.repositories:
            repo.safe_pull(self.user_account)
            repo.safe_push(self.user_account)

    def __schedule_push_pull_job(self, interval_mins=5):
        self.scheduler.start()
        # Schedule the daemon to push/pull all repos every 5 minutes
        self.push_pull_job = self.scheduler.add_job(self.__push_pull,
                'interval', minutes=interval_mins)

    # Returns a formated string representing the current time.
    def __get_timestamp(self): 
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S')

    # print the error to the log.
    def __get_user_account(self):
        try: 
            self.user_account = UserAccount(token_path='/tmp/gitup/token.txt')
        except ValueError as e:
            self.user_account = None
            print("{}: failed to create user account".format(
                    self.__get_timestamp()), file=sys.stderr)
            print(e, file=sys.stderr)

    # Parses the repository information stored in self.repofile, and stores the
    # Repostiory objects in self.repositories.
    def __parse_repositories(self):
        # if the repository file fails to open there is nothing we can do.
        repo_csv = None
        try:
            repo_csv = open(self.repofile, 'r')
        except Exception as e:
            print("{}: failed to open repofile".format(
                    self.__get_timestamp()), file=sys.stderr)
            print(e, file=sys.stderr)
            self.stop()
        csv_reader = csv.reader(repo_csv, delimiter=',')
        line = 0
        for row in csv_reader:
            if line != 0 or not row or not row[0]:
                path = row[0]
                try:
                    repo = Repository(path=path)
                    self.repositories.append(repo)
                except Exception as e:
                    print("repository for " + path + "failed to"
                        + " be initialized skipping", file=sys.stderr)
                    print(e, file=sys.stderr)
            line += 1

    # Begin watching for events in the repositories and forwarding
    # these events to the repositories. Does not return.
    def __watch_paths(self):
        paths = [ repo.path for repo in self.repositories ] 
        inotify = InotifyTrees(paths,mask=event_mask)
        # Watch events in repositories
        for event in inotify.event_gen(yield_nones=False):
            if self.__should_process_event(event):
                self.__handle_event(event)

    # Called when the daemon is started or restarted. May be called directly to
    # run the daemon connected to a terminal for easier testing.
    def run(self):
        self.__get_user_account()
        if not self.repofile:
            # A client might end up in the case if they don't pass a repofile to
            # the constructor. Allowing the user to not pass a repofile, makes
            # it easier for the user to construct the daemon when they only want
            # to stop it.
            print("run() called without providing a repofile", file=sys.stderr)
            self.stop() 
        # Parse repositories on every run to allow restarting to daemon to
        # update the repositories.
        self.__parse_repositories()
        if not self.repositories:
            print("run() called with an empty set of repositories",
                    file=sys.stderr)
            self.stop()
        # Notify the repositories that we are now watching them.
        for repo in self.repositories:
            repo.on_daemon_start(self.user_account)
        self.__schedule_push_pull_job()
        # Does not return.
        self.__watch_paths()

    # Returns True if the given type of file should be ignored, False
    # otherwise.
    def __ignores_file_type(self, filename):
        # For now we only ignore .swp files automatically.
        return filename.endswith(".swp") or filename.endswith(".swx")

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
    
    # Handle the given inotify event, finds the repository it pertains to
    # and forwards the event to that repository.
    def __handle_event(self, event):
        for repo in self.repositories:
             event_path = event[2]
             if repo.contains(event_path):
                 repo.handle_event(event, self.user_account)
 
