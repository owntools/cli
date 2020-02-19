from .shell import Shell

CLI_COMMANDS = [
    'run',
    'test',
    'debug',
    'logs',
    'clean',
    'nuke',
]


def run_cmd(cmd, dry_run=False, **kwargs):
    if dry_run:
        return print(cmd)

    sh = Shell(**kwargs)
    sh.exec(cmd)
    return sh
