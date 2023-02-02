#!/usr/bin/env python3
"""
logger module
"""


import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        format and log records
        """
        record.message = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        record.asctime = self.formatTime(record, self.datefmt)
        return self.FORMAT % {"name": record.name,
                              "levelname": record.levelname,
                              "asctime": record.asctime,
                              "message": record.message}
