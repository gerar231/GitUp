from gitup_daemon import GitUpDaemon

daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid')
daemon.stop()

