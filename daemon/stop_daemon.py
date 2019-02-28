#!/usr/bin/env python3.7
from daemon import GitUpDaemon

def stop_daemon():
    daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid')
    daemon.stop()

if __name__ == "__main__":
    stop_daemon()

