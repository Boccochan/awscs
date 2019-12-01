import os
import subprocess
from typing import List
from pathlib import Path

from awscs import config
from awscs import profile
from awscs import exception


def show_config():
    print("Current configurations:")
    conf = config.get_setting()

    if conf is None:
        print("No configuration")

    else:
        profile = conf['AWS_PROFILE']
        region = conf['AWS_DEFAULT_REGION']
        print(f'AWS_PROFILE: {profile}')
        print(f'AWS_PROFILE: {region}')


def run_cmd(cmd: str):
    show_config()
    conf = config.get_setting()
    print("------------------------")

    if conf is not None:
        os.environ['AWS_PROFILE'] = conf["AWS_PROFILE"]
        os.environ['AWS_DEFAULT_REGION'] = conf["AWS_DEFAULT_REGION"]

    subprocess.run(cmd, shell=True)


def _select_credentials(credentials: List[str]) -> str:
    print(f'\n--- credentials ---')

    for index, credential in enumerate(credentials, start=1):
        print('{0:<3} | {1:}'.format(index, credential))

    index = int(input('\nEnter the number:')) - 1

    num_of_credentials = len(credentials)
    if num_of_credentials < index or index < 0:
        print(f"Please enter the number from 1 to {num_of_credentials}")
        raise exception.WrongIndex

    return credentials[index]


def _select_default_region() -> str:
    regions = config.load_regions()
    print(f'\n--- regions ---')
    for index, region in enumerate(regions, start=1):
        print('{0:<2} | {1:}'.format(index, region))

    index = int(input('\nEnter the number:')) - 1

    num_of_regions = len(regions)

    if num_of_regions < index or index < 0:
        print(f"Please enter the number from 1 to {num_of_regions}")
        raise exception.WrongIndex

    return regions[index]


def run_setting() -> int:
    path = os.path.join(str(Path.home()), '.aws','credentials')
    credentials = profile.get_profiles(path)

    if not credentials:
        print(f'Not found credentials. Please check {path}')
        return 1

    show_config()

    try:
        credential = _select_credentials(credentials)
        region = _select_default_region()

    except exception.WrongIndex:
        return 2

    config.set_setting(credential, region)

    print('\n--------------------------')
    print('Saved config:')
    print(f'AWS_PROFILE: {credential}')
    print(f'AWS_DEFAULT_REGION: {region}')

    return 0
