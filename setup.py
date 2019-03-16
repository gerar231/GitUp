import sys
from cx_Freeze import setup, Executable

import os
PYTHON_INSTALL_DIR = os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

build_exe_options = {
    "packages": ["os", "idna", "pkg_resources"],
    "includes": ["git", "inotify", "apscheduler", "github", "csv", 
                 "inotify.adapters", "apscheduler.schedulers.background"],
    "include_files": ["./src/main/python/local_control", 
                      "./src/main/python/github_control",
                      "./src/main/python/daemon",
                      "./src/main/python/daemon_launcher",
                      "./src/main/python/gui/commit_grouper.py",
                      "./src/main/python/gui/lib"]
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name='GitUp', 
      version='0.1', 
      description='Simple Version Control', 
      options={"build_exe": build_exe_options},
      executables=[Executable("./src/main/python/gui/gui.py")])
