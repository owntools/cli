import argparse
from src import CLI_COMMANDS, make, prompt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='CLI for seamlessly switching between {API, SPA, Full-stack} boilerplates.',
        epilog='🔍 Found a bug? Please report it to https://github.com/owntools/cli',
    )
    parser.add_argument('command', nargs='?', help='command to run (default: prompt user for which boilerplate to use)', choices=['prompt', *CLI_COMMANDS], default='prompt')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='dry run only')
    parser.add_argument('--real', dest='dry_run', action='store_false', help='real run (opposite of --dry-run)')
    parser.set_defaults(dry_run=False)
    args = parser.parse_args()

    if args.command == 'prompt':
        prompt(args.dry_run)
    else:
        make(args.command, args.dry_run)
