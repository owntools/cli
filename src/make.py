from .util import CLI_COMMANDS, run_cmd


def run_make_command(cmd, dry_run):
    assert cmd in CLI_COMMANDS, f"Disallowed command: {cmd}"
    run_cmd(f"make {cmd}", dry_run=dry_run, die=True, verbose=True)
