import os
import sys
from select import select
from subprocess import Popen, PIPE


class CommandError(Exception):
    pass


class Shell:
    def __init__(self, cwd=None, die=False, verbose=False):
        self.cwd = cwd
        self.die = die
        self.verbose = verbose

        self.out = None

    def stream_output(self, p):
        readable = {
            p.stdout.fileno(): sys.stdout.buffer, # log separately
            p.stderr.fileno(): sys.stderr.buffer,
        }
        while readable:
            for fd in select(readable, [], [])[0]:
                data = os.read(fd, 1024) # read available
                if not data: # EOF
                    del readable[fd]
                else:
                    readable[fd].write(data)
                    readable[fd].flush()

    def exec(self, cmd):
        p = Popen(
            cmd,
            cwd=self.cwd,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        if self.verbose:
            self.stream_output(p)
            rc = p.poll()
        else:
            out, err = p.communicate()
            self.out = out
            rc = p.returncode

        if self.die and rc != 0:
            raise CommandError('exited non-zero')

    def output(self):
        assert not self.verbose, "Cannot retrieve output if verbose=True!"
        return self.out.decode('utf-8').splitlines()
