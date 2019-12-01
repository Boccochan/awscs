import os
import json
from pathlib import Path

from typing import Dict, Optional

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
