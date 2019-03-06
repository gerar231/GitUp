import sys
import os
from daemon import GitUpDaemon

tmp_csv_path = '/tmp/demo-repos.csv'
out = '/tmp/daemon.log'
err = '/tmp/dameon.err'
pidfile = '/tmp/gitup_daemon.pid'

if len(sys.argv) != 2:
    print("usage python demo.py <repository-directory>")
    exit(1)

repo_path = os.path.abspath(sys.argv[1])

# delte previous logs and csv
if os.path.isfile(out):
    os.remove(out)
if os.path.isfile(err):
    os.remove(err)
if os.path.isfile(tmp_csv_path):
   os.remove(tmp_csv_path)

tmp_csv_file = None
try:
    tmp_csv_file = open(tmp_csv_path, 'w+')
except IOError:
    print("failed to create new repository file")
    exit(1)

tmp_csv_file.write("local_path,last_pulled\n")
tmp_csv_file.write(repo_path + ",0\n")
tmp_csv_file.close()

daemon = GitUpDaemon(pidfile=pidfile,
                     repofile=tmp_csv_path,
                     stdout=out,
                     stderr=err)
daemon.start()


