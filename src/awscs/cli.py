import sys
import argparse
from awscs import handler
from awscs import exception

class Awscs:
    def __init__(self):
        self._parser = argparse.ArgumentParser(prog='Configure default credential')
        self._parser.add_argument('-s', action="store_true", default=False, help="Select profile")
        self._parser.add_argument('-c', action="store_true", default=False, help="Show current profile")
        self._args = self._parser.parse_args()

    def run(self) -> int:
        if self._args.s:
            try:
                handler.set_default_credential()

            except exception.AwscsException:
                return 1

            return 0

        elif self._args.c:
            return handler.show_config()

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
