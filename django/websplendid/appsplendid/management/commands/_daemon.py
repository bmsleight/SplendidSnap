#!/usr/bin/python
import time
from daemon import runner

import subprocess

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/lock/SplendidMaker.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
            args = ["/usr/bin/python", "/home/bms/SplendidSnap/django/websplendid/manage.py", "createpack"]
            p = subprocess.call(args)
            time.sleep(20)

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
