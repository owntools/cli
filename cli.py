import argparse
import sys
from src import CLI_COMMANDS, make, prompt


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='CLI for seamlessly switching between {API, SPA, Full-stack} boilerplates.',
        epilog='🔍 Found a bug? Please report it to https://github.com/owntools/cli',
        formatter_class=SmartFormatter,
    )
    fmt_opts = ''.join([f"    {k} = {v}\n" for k, v in CLI_COMMANDS.items()])
    parser.add_argument('command', nargs='?', choices=['help', 'prompt', *CLI_COMMANDS.keys()], default='prompt', help=f"R|Command to execute, where:\n"
         "    help = Show this help text\n"
         "    prompt* = Prompt user for boilerplate to use\n"
         f"{fmt_opts}"
         "* prompt is the default command")
    parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', help='dry run only')
    parser.set_defaults(dry_run=False)
    args = parser.parse_args()

    if args.command == 'help':
        parser.print_help()
        sys.exit(0)
    if args.command == 'prompt':
        prompt(args.dry_run)
    else:
        make(args.command, args.dry_run)
