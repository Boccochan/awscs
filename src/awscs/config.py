import os
import json
from pathlib import Path

from typing import Dict, Optional, List


DEFAULT_PATH = os.path.join(str(Path.home()), '.aws','.config.json')

def get_setting() -> Optional[Dict[str, str]]:
    try:
        with open(os.getenv('AWSCSPATH', DEFAULT_PATH), 'r') as f:
            json_data = json.load(f)

    except FileNotFoundError:
        return None

    return json_data


def set_setting(profile: str, region: str):
    with open(os.getenv('AWSCSPATH', DEFAULT_PATH), 'w') as f:
        json.dump({"AWS_PROFILE": profile, "AWS_DEFAULT_REGION": region}, f)


# def load_regions() -> List[str]:
#     # currently, regions list is fixed.
#     return [
#         'ap-northeast-1',
#         'us-east-1',
#         'ap-southeast-1',
#     ]
