# -*- coding: utf-8 -*-
"""The file contains some useful functions."""

from datetime import datetime
#from bondora.setup_logger import logger


def str_to_date(date_string):
    """
    Convert date string to datetime.date.

    Parameters
    ----------
    date_string : str
        String with date in format '%d.%m.%Y', '%Y-%m-%d', or '%Y%m%d'.

    Returns
    -------
    converted_date : datetime.date
        Date string converted in datetime.date.
    """
    # create format string
    if '.' in date_string:
        format_string = '%d.%m.%Y'
    elif '-' in date_string:
        format_string = '%Y-%m-%d'
    else:
        format_string = '%Y%m%d'

    # convert string to datetime.date
    try:
        converted_date = datetime.strptime(date_string, format_string).date()
        return converted_date

    except Exception as e:
        #logger.error(e)
        pass
