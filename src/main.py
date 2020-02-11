import os
import questionary as q

from .shell import Shell

BOILERPLATE_DIR = os.environ.get('BOILERPLATE_DIR', '/tmp/boilerplate')
INIT_BOILERPLATE = "INIT_BOILERPLATE"
NEW_CHALLENGE = "NEW_CHALLENGE"

APIS = ['express-api', 'flask-api']
LANGS = ['nodejs', 'python2', 'python3']
SPAS = ['react-app']


def run_cmd(cmd, dry_run=False, **kwargs):
    if dry_run:
        return print(cmd)

    sh = Shell(**kwargs)
    sh.exec(cmd)
    return sh


def get_bp_dirs():
    dirs = []
    for f in os.scandir(BOILERPLATE_DIR):
        if str(f.name).startswith('.'):
            continue
        if not f.is_dir():
            continue
        dirs.append(f.name)
    return dirs


def validate_bp_dir(init_boilerplate):
    """Git clone/pull latest owntools/boilerplate repo, and ensure boilerplate is in it."""
    boilerplate_dirs = get_bp_dirs()

    if boilerplate_dirs:
        # pull latest
        run_cmd('git fetch', cwd=BOILERPLATE_DIR, die=True)
        head_sha = run_cmd('git rev-parse HEAD', cwd=BOILERPLATE_DIR, die=True).output()[-1]
        current_sha = run_cmd('git rev-parse @{u}', cwd=BOILERPLATE_DIR, die=True).output()[-1]
        if head_sha != current_sha:
            run_cmd('git pull', cwd=BOILERPLATE_DIR, die=True)
            boilerplate_dirs = get_bp_dirs()
    else:
        # clone fresh
        try:
            run_cmd(f'git clone https://github.com/owntools/boilerplate.git {BOILERPLATE_DIR}', die=True)
        except CommandError:
            run_cmd(f'git clone git@github.com:owntools/boilerplate.git {BOILERPLATE_DIR}', die=True)
        boilerplate_dirs = get_bp_dirs()

    assert init_boilerplate in boilerplate_dirs, f"Sorry, {init_boilerplate} is not a valid boilerplate. See https://github.com/owntools/boilerplate for all available."


def sync_bp_dir(init_boilerplate, dry_run):
    """
    Copy the requested boilerplate from the owntools/boilerplate repo.

    Show the files that would be added/deleted, and prompt user for confirmation.
    """
    init_tmpl = f"rsync %s --delete --exclude '.git' --exclude 'node_modules' {BOILERPLATE_DIR}/{init_boilerplate}/ {os.getcwd()}"
    init_preview = init_tmpl % '-anv'
    init_real = init_tmpl % '-av'

    run_cmd(init_preview, dry_run=False, verbose=True, die=True)
    if dry_run:
        run_cmd(init_real, dry_run=True, verbose=True, die=True)
    else:
        confirm_init = q.confirm("This will replace all files in current directory with the above files. Continue?", default=False).ask()
        if confirm_init:
            run_cmd(init_real, dry_run=False, verbose=True, die=True)


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

    validate_bp_dir(init_boilerplate)
    sync_bp_dir(init_boilerplate, dry_run)
