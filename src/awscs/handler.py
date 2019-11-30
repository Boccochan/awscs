import os
import re
from pathlib import Path

from typing import List, Optional

from awscs import config

pattern = r'\s*\[.+\][\s]*$'
regex = re.compile(pattern)


class AwscsException(Exception):
    ''' This is the base exception class for awscs'''


class WrongIndex(AwscsException):
    ''' User inputs wrong index '''


def _remove_brackets(words: str) -> str:
    return words.split('[', 1)[-1].rsplit(']', 1)[0]


def get_credentials(path: str) -> List[str]:
    credentials = []
    with open(path, 'r') as f:
        for line in f.readlines():
            if regex.match(line) is not None:
                credential = _remove_brackets(line)
                credentials.append(credential)

    return credentials


def _show_config():
    print("Current configurations")
    conf = config.get_setting()

    print(conf)

    if conf is None:
        print("No configuration")
    else:
        profile = conf['AWS_PROFILE']
        region = conf['AWS_DEFAULT_REGION']
        print(f'AWS_PROFILE: {profile}')
        print(f'AWS_PROFILE: {region}')


def _select_credentials(credentials: List[str]) -> str:
    print(f'--- credentials ---')

    for index, credential in enumerate(credentials, start=1):
        print('{0:<3} | {1:}'.format(index, credential))

    index = int(input('Enter the number:')) - 1

    num_of_credentials = len(credentials)
    if num_of_credentials < index or index < 0:
        print(f"Please enter the number from 1 to {num_of_credentials + 1}")
        raise WrongIndex

    return credentials[index]


def _select_default_region() -> str:
    regions = config.load_regions()
    print(f'--- regions ---')
    for index, region in enumerate(regions, start=1):
        print('{0:<2} | {1:}'.format(index, region))

    index = int(input('Enter the number:')) - 1

    num_of_regions = len(regions)

    if num_of_regions < index or index < 0:
        print(f"Please enter the number from 1 to {num_of_regions + 1}")
        raise WrongIndex

    return regions[index]


def run() -> int:
    path = os.path.join(str(Path.home()), '.aws','credentials')
    credentials = get_credentials(path)

    if not credentials:
        print(f'Not found credentials. Please check {path}')
        return 1

    _show_config()

    try:
        profile = _select_credentials(credentials)
        region = _select_default_region()

    except WrongIndex:
        return 2

    config.set_setting(profile, region)

    print('--------------------------')
    print('Saved config:')
    print(f'AWS_PROFILE: {profile}')
    print(f'AWS_DEFAULT_REGION: {region}')

    return 0
