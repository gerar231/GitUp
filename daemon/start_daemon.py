from gitup_daemon import GitUpDaemon
import os

logs_dir_path = '/tmp/gitup/'
out_path = '/tmp/gitup/daemon.out'
err_path = '/tmp/gitup/daemon.err'

# make sure the directory to write logs to exists.
if not os.path.isdir(logs_dir_path):
    try:
        os.mkdir(logs_dir_path)
    except:
        print "failed to create logs directory"
        exit(1)
# delte previous logs
if os.path.isfile(out_path):
    os.remove(out_path)
if os.path.isfile(err_path):
    os.remove(err_path)
daemon = GitUpDaemon(pidfile='/tmp/gitup_daemon.pid',
                     stdout=out_path,
                     stderr=err_path)
daemon.start()

