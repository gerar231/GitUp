#!/usr/bin/env python3.7
from .daemon import GitUpDaemon

def restart_daemon():
    repofile = "/tmp/gitup/repositories.csv"
    logs_dir = '/tmp/gitup/'
    out = '/tmp/gitup/daemon.out'
    err = '/tmp/gitup/daemon.err'
    daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid',
                         repofile=repofile,
                         stdout=out,
                         stderr=err)
    daemon.restart()

if __name__ == "__main__":
    restart_daemon()

