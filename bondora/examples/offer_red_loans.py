#!/opt/miniconda3/envs/flask/bin/python
# -*- coding: utf-8 -*-
"""Example how to offer defaulted (red) loans on bondora's secondary market."""

import os
import sys
import inspect
import configparser
from datetime import datetime, timedelta

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from setup_logger import logger
from trading.bondora_trading import BondoraTrading

PATH_SETTINGS = '/var/www/flask/bondora/settings.cfg'

price = -85 # selling price (-85%)


# read configuration
try:
    logger.info('Reading configuration from {}...'.format(PATH_SETTINGS))
    config = configparser.ConfigParser()
    config.read_file(open(PATH_SETTINGS))

    TOKEN = config.get('BONDORA', 'TOKEN')

except Exception as e:
    logger.critical(e)
    sys.exit(-1)


def offer_red_loans(token, price, retry=True):
    """
    Offer defaulted (red) loans on bondora's secondary market for selling.

    Parameters
    ----------
    token : str
        Access token.
    price : int
        Price to sell loan.
    retry : bool, optional
            Retry to execute the underlying methods, if too many requests.
            The default is True.

    Returns
    -------
    None.

    """
    # initialize trading object
    bt = BondoraTrading(token)

    # calcel secondary market offering of loans
    # with defaulted loans status
    # and latest debt management stage type of write off
    # and last payment date not within last 12 months
    last_payment = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    bt.cancel_sm_offers(retry=retry,
                        last_payment_date=last_payment,
                        LoanStatusCode=5,
                        LoanDebtManagementStageType=3)

    # place these loans on secondary market for selling
    bt.place_sm_offers(max_price=price,
                       retry=retry,
                       last_payment_date=last_payment,
                       LoanStatusCode=5,
                       LoanDebtManagementStageType=3)


if __name__ == "__main__":
    offer_red_loans(TOKEN, price)
