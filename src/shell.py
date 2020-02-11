import subprocess


class CommandError(Exception):
    pass


class Shell:
    def __init__(self, cwd=None, die=False, verbose=False):
        self.cwd = cwd
        self.die = die
        self.verbose = verbose

        self.rc = None
        self.out = None
        self.err = None

    def exec(self, cmd):
        pipes = subprocess.Popen(
            cmd,
            cwd=self.cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = pipes.communicate()
        self.rc = pipes.returncode
        self.out = out
        self.err = err

        if self.verbose:
            for l in self.output():
                print(l)
            for l in self.errors():
                print(l)

        if self.die and self.rc != 0:
            raise CommandError(self.get_last_err())

    def output(self):
        return self.out.decode('utf-8').splitlines()

    def errors(self):
        return self.err.decode('utf-8').splitlines()

    def get_last_err(self):
        last_err = 'exit code non-zero'
        for line in self.errors():
            clean_line = line.strip()
            if clean_line:
                last_err = clean_line

        return last_err
