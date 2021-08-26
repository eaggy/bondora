# -*- coding: utf-8 -*-
"""The file contains the class definition of Bondora data loader."""

import re
import os
import sys
import inspect
import pickle
import zipfile
from datetime import datetime, timedelta
from io import BytesIO
from urllib.request import urlopen, Request
import pandas as pd

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from setup_logger import logger
from toolkit import str_to_date


URL_DATA = 'https://www.bondora.com/marketing/media/ResaleArchive.zip'


class DataLoader(object):
    """Class representation of data loader."""

    def __init__(self, start_date=None, end_date=None):
        """
        Call constructor of class.

        Parameters
        ----------
        start_date : datetime.date, optional
            Start date of transactions to select. The default is None.
        end_date : datetime.date, optional
            End date of transactions to select. The default is None.

        Returns
        -------
        None.

        """
        # convert `end_date` to datetime.date
        if end_date:
            end_date = str_to_date(end_date)
            if not end_date:
                # set `end_date` as today
                end_date = datetime.now().date()
        self.end_date = end_date

        # convert `start_date` to datetime.date
        if start_date:
            start_date = str_to_date(start_date)
            if not start_date:
                # set `start_date` as today - 365 days
                start_date = (datetime.now() - timedelta(days=365)).date()
        self.start_date = start_date

        self.data = None

    def _unzip(self, file):
        """
        Read zipped csv-file into pandas DataFrame.

        Parameters
        ----------
        file : string
            The path to zip-archive.

        Returns
        -------
        df : pandas.core.frame.DataFrame
            DataFrame containing data from archived csv-file.

        """
        with zipfile.ZipFile(file) as zip_file:
            try:
                df = pd.read_csv(zip_file.open(
                    zip_file.infolist()[0].filename))
                return df

            except Exception as e:
                logger.error(e)

    def download_data(self):
        """
        Download zipped data from internet and unzip it.

        Returns
        -------
        None.

        """
        headers = {'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) '
                                  'AppleWebKit/537.11 (KHTML, like Gecko) '
                                  'Chrome/23.0.1271.64 Safari/537.11'),
                   'Accept': ('text/html,application/xhtml+xml,'
                              'application/xml;q=0.9,*/*;q=0.8'),
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}

        try:
            request = Request(URL_DATA, None, headers)
            response = urlopen(request)
            self.data = self._unzip(BytesIO(response.read()))

        except Exception as e:
            logger.error(e)

    def process_data(self):
        """
        Select important columns and rows between `start_date` and `end_date`.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        df = pd.DataFrame()

        try:
            # select important columns and rows corresponding
            # to successful transactions (`Result` == 'Successful')
            columns = ['loan_id', 'PrincipalAtEnd',
                       'DiscountRate', 'StartDate', 'EndDate']
            df = self.data.loc[self.data['Result'] == 'Successful', columns]

            # convert column type from string to datetime format
            df['StartDate'] = pd.to_datetime(df['StartDate'])
            df['EndDate'] = pd.to_datetime(df['EndDate'])

            # select transactions realized after or on start_date
            if self.start_date:
                df = df.loc[df['EndDate'].dt.date >= self.start_date, :]

            # select transaction realized before or on end_date
            if self.end_date:
                df = df.loc[df['EndDate'].dt.date <= self.end_date, :]

            # remove transactions with `DiscountRate` > 100%
            df = df.loc[df['DiscountRate'] <= 100., :]

            # set `DiscountRate` as integer
            df['DiscountRate'] = df['DiscountRate'].astype(int)

            # remove '{' and '}' from 'loan_id' column
            df['loan_id'] = df['loan_id'].apply(
                lambda x: re.sub(r'[\{\}]', '', x))

            # calculate time (in seconds) how long a loan was offered for sale
            df['OfferTime'] = (df['EndDate'] - df['StartDate']).astype(
                'timedelta64[s]')

            # reset index
            df.reset_index(drop=True, inplace=True)

            self.data = df

        except Exception as e:
            logger.error(e)

    def save_data(self, path):
        """
        Save DataFrame to file.

        Parameters
        ----------
        path : str
            Path to save data.

        Returns
        -------
        None.

        """
        if self.data is not None:
            with open(path, 'wb') as handle:
                pickle.dump(self.data,
                            handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
