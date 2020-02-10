import argparse
import os
import questionary as q
from prompt_toolkit.styles import Style
from shell import shell

INIT_BOILERPLATE = "INIT_BOILERPLATE"
NEW_CHALLENGE = "NEW_CHALLENGE"
OTHER = "OTHER"
BOILERPLATE_DIR = os.environ.get('BOILERPLATE_DIR', '/tmp/boilerplate')

APIS = ['express-api', 'flask-api']
LANGS = ['nodejs', 'python2', 'python3']
SPAS = ['react-app']


def run_cmd(cmd, dry_run, **kwargs):
    if dry_run:
        return print(cmd)

    return shell(cmd, **kwargs)


def main(dry_run):
    action = q.select(
        "What do you want to do?",
        choices=[
            {"name":"init boilerplate", "value": INIT_BOILERPLATE},
            {"name":"create a new challenge", "value": NEW_CHALLENGE},
        ],
    ).ask()

    init_boilerplate = q.select(
        "Which boilerplate do you want to use?",
        choices=[
            q.Separator("---API---"),
            *APIS,
            q.Separator("---langs---"),
            *LANGS,
            q.Separator("---SPA---"),
            *SPAS,
        ],
    ).ask()

    api_choices = [q.Choice(x, checked=True) for x in APIS] if init_boilerplate in APIS else APIS
    lang_choices = [q.Choice(x, checked=True) for x in LANGS] if init_boilerplate in LANGS else LANGS
    spa_choices = [q.Choice(x, checked=True) for x in SPAS] if init_boilerplate in SPAS else SPAS

    while action == NEW_CHALLENGE:
        allowed_boilerplates = q.checkbox(
            "Which boilerplates are candidates allowed to use?",
            choices=[
                q.Separator("---API---"),
                *api_choices,
                q.Separator("---langs---"),
                *lang_choices,
                q.Separator("---SPA---"),
                *spa_choices,
            ],
        ).ask()

        confirm_none = q.confirm(
            "No allowed boilerplates. Are you sure?",
            default=False,
        ).skip_if(len(allowed_boilerplates)).ask()

        if len(allowed_boilerplates) or confirm_none:
            break

    ls = run_cmd(f'ls {BOILERPLATE_DIR}', dry_run=False)
    boilerplate_dirs = list(ls.output())
    if not boilerplate_dirs:
        try:
            run_cmd(f'git clone https://github.com/owntools/boilerplate.git {BOILERPLATE_DIR}', dry_run=dry_run, die=True)
        except Exception:
            run_cmd(f'git clone git@github.com:owntools/boilerplate.git {BOILERPLATE_DIR}', dry_run=dry_run, die=True)

        ls = run_cmd(f'ls {BOILERPLATE_DIR}', dry_run=False)
        boilerplate_dirs = list(ls.output())

    assert init_boilerplate in boilerplate_dirs, f"Sorry, {init_boilerplate} is not a valid boilerplate. See https://github.com/owntools/boilerplate for all available."

    init_tmpl = f"rsync %s --delete --exclude '.git' --exclude 'node_modules' {BOILERPLATE_DIR}/{init_boilerplate}/ {os.getcwd()}"
    init_preview = init_tmpl % '-anv'
    init_real = init_tmpl % '-av'

    run_cmd(init_preview, dry_run=False, verbose=True, die=True)
    if not dry_run:
        confirm_init = q.confirm("Continue?", default=False).ask()
        if confirm_init:
            run_cmd(init_real, dry_run=False, verbose=True, die=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the owntools CLI to create/solve programming challenges with your own tools.')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true')
    parser.add_argument('--real', dest='dry_run', action='store_false')
    parser.set_defaults(dry_run=False)
    args = parser.parse_args()

    main(args.dry_run)
