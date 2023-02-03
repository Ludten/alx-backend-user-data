#!/usr/bin/env python3
"""
logger module
"""


import logging
import os
import mysql.connector
import re
from typing import List

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


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


def get_logger() -> logging.Logger:
    """
    log and format data
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    h1 = logging.StreamHandler()
    h1.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(h1)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    create a connection to the database
    """
    mydb = mysql.connector.connect(
        host=os.environ["PERSONAL_DATA_DB_HOST"],
        database=os.environ["PERSONAL_DATA_DB_NAME"],
        user=os.environ["PERSONAL_DATA_DB_USERNAME"],
        password=os.environ["PERSONAL_DATA_DB_PASSWORD"]
    )
    return mydb


def main():
    """
    program entry point
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        logger = get_logger()
        msg = "name={}; email={}; phone={}; ssn={}; password={}; ip={};\
 last_login={}; user_agent={}".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
