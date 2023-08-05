# (The MIT License)
#
# Copyright (c) 2016 Kura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
blackhole.daemon.

Provides daemon functional to blackhole.
"""


import os
import atexit

from blackhole.exceptions import DaemonException


class Singleton(type):
    """A singleton for :any:`blackhole.daemon.Daemon`."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        A singleton for :any:`blackhole.daemon.Daemon`.

        :param cls:
        :type cls: :any:`blackhole.daemon.Daemon`
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class Daemon(metaclass=Singleton):
    """An object for handling daemonisation."""

    def __init__(self, pidfile):
        """
        Create an instance of :any:`blackhole.daemon.Daemon`.

        :param pidfile:
        :type pidfile: :any:`str`
        """
        self.pidfile = pidfile

    def daemonize(self):
        """
        Daemonize the process, using the UNIX double fork method.

        .. note::

           Registers an :any:`atexit.register` signal to delete the pid on
           exit.
        """
        self.fork()
        os.chdir(os.path.sep)
        os.setsid()
        os.umask(0)
        self.fork()
        atexit.register(self._delpid)
        self.pid = os.getpid()

    def _delpid(self):
        """
        Wrapper around :any:`del self.pid` for use with :any:`atexit.register`.

        This is not a public method for API use.
        """
        del self.pid

    def fork(self):
        """
        Fork off the process.

        :raises: :any:`SystemExit` -- :any:`os.EX_OK`
        :raises: :any:`blackhole.exceptions.DaemonException`
        """
        try:
            pid = os.fork()
            if pid > 0:
                raise SystemExit(os.EX_OK)
        except OSError as err:
            raise DaemonException(err.strerror)

    @property
    def pid(self):
        """
        The pid of the process, if it's been daemonised.

        :raises: :any:`blackhole.exceptions.DaemonException` if pid cannot be
                 read from the filesystem.
        :returns: :any:`int` or :any:`None` if no pid.

        .. note::

           The pid is retrieved from the filestem.
           If the pid does not exist in /proc, the pid is deleted.
        """
        if os.path.exists(self.pidfile):
            try:
                pid = open(self.pidfile, 'r').read().strip()
                if pid != '':
                    return int(pid)
            except (FileNotFoundError, IOError, PermissionError,
                    OSError) as err:
                raise DaemonException(err.strerror)
        return None

    @pid.setter
    def pid(self, pid):
        """
        Write the pid to the filesystem.

        :raises: :any:`daemon.daemon.DaemonException` if writing to filesystem
                 fails.
        :param pid: the process's pid.
        :type pid: :any:`int`
        """
        pid = str(pid)
        try:
            with open(self.pidfile, 'w+') as pidfile:
                pidfile.write("{}\n".format(pid))
        except (IOError, FileNotFoundError, PermissionError) as err:
            raise DaemonException(err.strerror)

    @pid.deleter
    def pid(self):
        """Delete the pid from the filesystem."""
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
