#!/usr/bin/env python3
"""
logger module
"""


import re
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Return log message
    """
    for field in fields:
        pattern = "(?<={}=).*?(?={})".format(field, separator)
        message = re.sub(pattern, redaction, message)
    return message
