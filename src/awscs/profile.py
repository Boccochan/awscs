import re
import os
from pathlib import Path

from typing import List


pattern = r'\s*\[.+\][\s]*$'
regex = re.compile(pattern)


def _remove_brackets(words: str) -> str:
    return words.split('[', 1)[-1].rsplit(']', 1)[0]


def get_profiles(path: str) -> List[str]:
    profiles = []
    with open(path, 'r') as f:
        for line in f.readlines():
            if regex.match(line) is not None:
                profile = _remove_brackets(line)
                profiles.append(profile)

    return profiles
