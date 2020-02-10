import questionary as q
from prompt_toolkit.styles import Style

INIT_BOILERPLATE = "INIT_BOILERPLATE"
NEW_CHALLENGE = "NEW_CHALLENGE"
OTHER = "OTHER"

APIS = ['express-api', 'flask-api']
LANGS = ['nodejs', 'python2', 'python3']
SPAS = ['react-app']


def main():
    action = q.select(
        "What do you want to do?",
        choices=[
            {"name":"init boilerplate", "value": INIT_BOILERPLATE},
            {"name":"create a new challenge", "value": NEW_CHALLENGE},
            {"name":"do something else", "value": OTHER},
        ],
    ).ask()

    if action == OTHER:
        return print(f"Sorry, I can't do {action}. Bye! 👋")

    boilerplate = q.select(
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

    api_choices = [q.Choice(x, checked=True) for x in APIS] if boilerplate in APIS else APIS
    lang_choices = [q.Choice(x, checked=True) for x in LANGS] if boilerplate in LANGS else LANGS
    spa_choices = [q.Choice(x, checked=True) for x in SPAS] if boilerplate in SPAS else SPAS

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


if __name__ == "__main__":
    main()
