import sys
import os
from ../daemon/daemon import GitUpDaemon

tmp_csv_path = '/tmp/demo-repos.csv'
stdin = '/tmp/daemon.log'
stdout = '/tmp/dameon.err'
pidfile = '/tmp/gitup_daemon.pid'

if len(sys.argv) != 2:
    print "usage python demo.py <repository-directory>"
    exit(1)

repo_path = os.path.abspath(sys.argv[1])
tmp_csv_file = None
try
    tmp_csv_file = open(tmp_csv_path, 'w+')
except IOError:
    print "failed to create repository file"
    exit(1)

tmp_csv_file.write("local_path,last_pulled\n")
tmp_csv_file.write(repo_path + ",0\n")
tmp_csv_file.close()

daemon = GitUpDaemon(pidfile=pidfile
                     repofile=tmp_csv_path,
                     stdin=stdin,
                     stdout=stdout)
daemon.start()
os.remove(tmp_csv_path)


