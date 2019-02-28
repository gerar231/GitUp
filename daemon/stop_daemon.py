#!/usr/bin/env python3.7
from daemon import GitUpDaemon

daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid')
daemon.stop()

