import re
import sys
import os
from pathlib import Path
from shutil import copyfile
from typing import List
from awscs import exception

DEFAULT_TEMPLATE_PATH = os.path.join(str(Path.home()), '.aws','.credentials')
DEFAULT_PROFILE_PATH = os.path.join(str(Path.home()), '.aws','credentials')

pattern = r'\s*\[.+\][\s]*$'
regex = re.compile(pattern)


def _remove_brackets(words: str) -> str:
    return words.split('[', 1)[-1].rsplit(']', 1)[0]


def load(path: str) -> List[str]:
    profiles = []

    try:
        with open(path, 'r') as f:
            for line in f.readlines():
                if regex.match(line) is not None:
                    profile = _remove_brackets(line)
                    profiles.append(profile)

    except FileNotFoundError as e:
        msg = f"Not found tag such as [test_env]. Please check {DEFAULT_PROFILE_PATH}"
        print(msg, file=sys.stderr)
        raise exception.NotFoundFile(e)

    if 'default' in profiles:
        msg = f"{DEFAULT_PROFILE_PATH} does not exist"
        print(msg, file=sys.stderr)
        raise exception.FoundDefault

    if not profiles:
        msg = f"Found default tag in {DEFAULT_PROFILE_PATH}"
        print(msg, file=sys.stderr)
        raise exception.NotFoundTag

    return profiles


def set_default(target: str):
    credential_data = []

    try:
        with open(os.getenv('AWSCS_TEMPLATE_CREDENTIALS', DEFAULT_TEMPLATE_PATH), 'r') as f:
            for line in f.readlines():
                if regex.match(line) is not None:
                    profile = _remove_brackets(line)
                    if profile == target:
                        line = '[default]\n'

                credential_data.append(line)

        with open(os.getenv('AWSCS_PROFILE_PATH', DEFAULT_PROFILE_PATH), 'w') as f:
            f.write(''.join(credential_data))

    except FileNotFoundError:
        pass


def copy():
    src = os.getenv('AWSCS_PROFILE_PATH', DEFAULT_PROFILE_PATH)
    dst = os.getenv('AWSCS_TEMPLATE_CREDENTIALS', DEFAULT_TEMPLATE_PATH)

    if os.path.isfile(dst):
        return

    try:
        copyfile(src, dst)

    except FileNotFoundError as e:
        print(f'Not found {src}')
        print("Please run \"aws configure\"")
        raise exception.NotFoundFile(e)
