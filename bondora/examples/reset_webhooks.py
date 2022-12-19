#!/opt/miniconda3/envs/flask/bin/python
# -*- coding: utf-8 -*-
"""Example how to reset webhooks via web interface."""

import os
import sys
import time
import inspect
import configparser
from random import randrange

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from setup_logger import logger
from hooks.application import BondoraApplication

PATH_SETTINGS = '/var/www/flask/bondora/settings.cfg'

# maximal number of failures
threshold = 5

# shift execution randomly between 0 and 60 seconds
randomize = 60

# read configuration
try:
    logger.info('Reading configuration from {}...'.format(PATH_SETTINGS))
    config = configparser.ConfigParser()
    config.read_file(open(PATH_SETTINGS))

    USER_NAME = config.get('BONDORA', 'USER')
    USER_PASSWORD = config.get('BONDORA', 'PASSWORD')
    APPLICATION_ID = config.get('BONDORA', 'APPLICATION_ID')

except Exception as e:
    logger.critical(e)
    sys.exit(0)


def reset_webhooks(user, password, application_id, threshold, randomize=0):
    """
    Reset webhooks, if the number of failures are above threshold.

    Parameters
    ----------
    user : str
        User e-mail.
    password : str
        User password.
    application_id : str
        Application ID.
    threshold : int
            Threshold for maximal number of failures.
    randomize : int, optional
         Maximal number of seconds of random number generator for
         a waiting before proceed. The default is 0.

    Returns
    -------
    None.

    """
    # wait random number of seconds before proceeding
    if randomize > 0:
        time.sleep(randrange(randomize))

    # initialize  object
    bw = BondoraApplication(user, password, application_id)

    # get webhooks
    bw.get_webhooks()

    # reset webhooks
    bw.reset_webhooks(threshold)


if __name__ == "__main__":
    reset_webhooks(USER_NAME, USER_PASSWORD, APPLICATION_ID,
                   threshold, randomize)
