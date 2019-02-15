from gitup_daemon import GitUpDaemon

daemon = GitUpDaemon('/usr/run/gitup_daemon.pid')
daemon.start()


