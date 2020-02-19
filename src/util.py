from .shell import Shell

CLI_COMMANDS = {
    'run': 'Run the program',
    'test': 'Test/check your solution',
    'debug': 'Run your program, stopping at debug breakpoints',
    'logs': 'Show all logs for your program',
    'clean': 'Clean docker containers for current boilerplate',
    'nuke': 'Kill all docker containers (useful if port 8080 is blocked by something)',
}


def run_cmd(cmd, dry_run=False, **kwargs):
    if dry_run:
        return print(cmd)

    sh = Shell(**kwargs)
    sh.exec(cmd)
    return sh
