#Compile the python files in /src folder
cd src
python3.7 -m compileall -l .

#Compile the python files in /src/main/python/gui
python3.7 -m compileall -l ./main/python/gui

#Compile the python files in /src/main/python/daemon
python3.7 -m compileall -l ./main/python/daemon

#Compile the python files in /src/main/python/daemon_launcher
python3.7 -m compileall -l ./main/python/daemon_launcher

#Compile the python files in /src/main/python/github_control
python3.7 -m compileall -l ./main/python/github_control

#Compile the python files in /src/main/python/local_control
python3.7 -m compileall -l ./main/python/local_control

#Compile the python files in /src/unittest/python
python3.7 -m compileall -l ./unittest/python
