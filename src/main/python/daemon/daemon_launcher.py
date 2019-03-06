#!/usr/bin/env python3.7
import os
import sys
from .daemon import GitUpDaemon
    
repofile = "/tmp/gitup/repositories.csv"
logs_dir = '/tmp/gitup/'
out = '/tmp/gitup/daemon.out'
err = '/tmp/gitup/daemon.err'

def start_daemon():
    # make sure the directory to write logs to exists.
    if not os.path.isdir(logs_dir):
        try:
            os.mkdir(logs_dir)
        except OSError:
            print >> os.stderr,("failed to create logs directory")
            exit(1)
    # delte previous logs
    if os.path.isfile(out):
        os.remove(out)
    if os.path.isfile(err):
        os.remove(err)
    daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid',
                         repofile=repofile,
                         stdout=out,
                         stderr=err)
    # Change this to daemon.run() to run the daemon connected to
    # the terminal for easier debugging
    daemon.run()

def stop_daemon():
    daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid')
    daemon.stop()

def restart_daemon():
    daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid',
                         repofile=repofile,
                         stdout=out,
                         stderr=err)
    daemon.restart()

def usage():
    print('usage ./daemon_launcher.py start|stop|restart')
 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit(1)
    if sys.argv[1] == 'start':  
        start_daemon()
    elif sys.argv[1] == 'stop':
        stop_daemon()
    elif sys.argv[1] == 'restart':
        restart_daemon()
    else:
        print("invalid option {}".format(sys.argv[1]))
        usage()
        exit(1)

