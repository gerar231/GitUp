import sys
import os
import time
import subprocess
from git import Repo
from git.exc import GitCommandError
sys.path.append(os.path.normpath("../../main/python/"))
from daemon_launcher import daemon_launcher
from multiprocessing import Process

subprocess.call("./initrepo.sh")

try:
    repo = Repo('/tmp/testrepo/')
except GitCommandError:
    print('failed to get access to repo through git python')
    exit(1)

# Make sure the daemon isn't running when we start
if daemon_launcher.daemon_is_running():
    daemon_launcher.stop_daemon()

# Start the daemon and wait for this action to finish
p = Process(target=daemon_launcher.start_daemon)
p.start()
p.join()
time.sleep(1)

# add a file to repo
f = None
try:
    f = open('/tmp/testrepo/testfile.py', 'w+')
except IOError:
    print('failed to open file')
    exit(1)
# write a method header to get the first commit
f.write('def testmethod():')
f.close()
# give the daemon time to make a commit
time.sleep(1)

# check that the commit happenend and that it has the right method
commits = [ c for c in repo.iter_commits() ]
assert len(commits) == 1, ("commits had length {}, expected 1"
        .format(len(commits)))
commit = commits[0]
stripped_commit_message = commit.message.strip()
assert stripped_commit_message == 'testfile.py', ("commit had message {}, expected testfile.py"
        .format(stripped_commit_message))

# reopen the file and edit the method
try:
    f = open('/tmp/testrepo/testfile.py', 'w+')
except IOError:
    print('failed to open file')
    exit(1)
f.write('    print(\'hi\')')
f.close()
# give the daemon time to make a commit
time.sleep(1)

# check that both commits are present
commits = [ c for c in repo.iter_commits() ]
assert len(commits) == 2, ("commits had length {}, expected 2"
        .format(len(commits)))
commit = commits[0]
stripped_commit_message = commit.message.strip()
assert stripped_commit_message == 'testfile.py', ("commit had message {}, expected testfile.py"
        .format(stripped_commit_message))
# TODO uncomment this once commit message bug is fixed
# commit = commits[1]
# stripped_commit_message = commit.message.strip()
# assert stripped_commit_message == 'testfile.py: def testmethod():', (("commit had message {}\n" + 
#        "expected testfile.py: def testmethod():").format(stripped_commit_message))

daemon_launcher.stop_daemon()

print('passed')
exit(0)

