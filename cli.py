import argparse
from src.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the owntools CLI to create/solve programming challenges with your own tools.')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true')
    parser.add_argument('--real', dest='dry_run', action='store_false')
    parser.set_defaults(dry_run=False)
    args = parser.parse_args()

    main(args.dry_run)
