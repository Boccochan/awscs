import sys
import argparse
from awscs import handler


class Awscs:
    def __init__(self):
        self._parser = argparse.ArgumentParser(prog='Configure AWS_PROFILE/AWS_DEFAULT_REGION', usage="awscs aws s3 ls")
        self._parser.add_argument('-s', action="store_true", default=False, help="Select profile and region")
        self._parser.add_argument('-c', action="store_true", default=False, help="Show current profile and region")
        self._parser.add_argument('cmd', nargs='*', help='Execute command with AWS_PROFILE/AWS_DEFAULT_REGION')
        self._args = self._parser.parse_args()

    def run(self) -> int:
        if self._args.s:
            return handler.run_setting()

        elif self._args.c:
            return handler.show_config()

        elif self._args.cmd:
            return handler.run_cmd(' '.join(self._args.cmd))

        self._parser.print_help()

        return 0


def main():
    awscs = Awscs()

    try:
        result = awscs.run()

    except KeyboardInterrupt:
        return 5

    return result


if __name__ == "__main__":
    sys.exit(main())
