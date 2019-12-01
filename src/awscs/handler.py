from typing import List

from awscs import config
from awscs import exception
from awscs import credential as crd


def show_config():
    print("-------------------")
    print("Current default profile: ", end="")
    conf = config.get_setting()

    if conf is None:
        print("No configuration")

    else:
        profile = conf['AWS_PROFILE']
        print(f'{profile}')


def _select_credentials(credentials: List[str]) -> str:
    print(f'\n--- credentials ---')

    for index, tag in enumerate(credentials, start=1):
        print('{0:<3} | {1:}'.format(index, tag))

    num_of_credentials = len(credentials)

    try:
        index = int(input('\nEnter the number:')) - 1

    except ValueError:
        print(f'Please enter number from 1 to {num_of_credentials}')
        raise exception.WrongInput

    if index >= num_of_credentials  or index < 0:
        print(f"Please enter the number from 1 to {num_of_credentials}")
        raise exception.WrongIndex

    return credentials[index]


def set_default_credential():
    crd.copy()
    profiles = crd.load(crd.DEFAULT_TEMPLATE_PATH)

    show_config()

    tag = _select_credentials(profiles)
    crd.set_default(tag)

    config.set_setting(tag, '')
    show_config()
