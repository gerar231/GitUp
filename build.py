from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("python.unittest")

name = "GitUp"
default_task = "publish"

@init
def initialize(project):
    project.build_depends_on('PyGitHub')
    project.build_depends_on('GitPython')
    project.build_depends_on('inotify')
    project.build_depends_on('apscheduler')
