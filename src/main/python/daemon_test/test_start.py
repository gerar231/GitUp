import sys
import os
import time
sys.path.append(os.path.normpath(".."))
from daemon_launcher import daemon_launcher
from multiprocessing import Process

# Make sure the daemon isn't running when we start
if daemon_launcher.daemon_is_running():
    daemon_launcher.stop_daemon()

# Start the daemon and wait for this action to finish
p = Process(target=daemon_launcher.start_daemon)
p.start()
p.join()
time.sleep(1)


# check that the daemon is running.
assert(daemon_launcher.daemon_is_running())
# check that the log files exist.
assert(os.path.isfile('/tmp/gitup/daemon.out'))
assert(os.path.isfile('/tmp/gitup/daemon.err'))

# stop the daemon
daemon_launcher.stop_daemon()

print('passed')
exit(0)

