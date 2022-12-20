# -*- coding: utf-8 -*-
"""The file contains the class definition of Bondora data loader."""

import pickle
import zipfile
from datetime import datetime, timedelta
from io import BytesIO
from urllib.request import urlopen, Request
import pandas as pd
from bondora.setup_logger import logger
from utils.datetime_utils import str_to_date

pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 1000)

URL_DATA_RESALES = 'https://www.bondora.com/marketing/media/ResaleArchive.zip'
URL_DATA_LOANS = "https://www.bondora.com/marketing/media/LoanData.zip"


class DataLoader:
    """Class representation of data loader."""

    def __init__(self, start_date, end_date):
        """
        Initialize the class instance.

        Parameters
        ----------
        start_date : str
            Start date of transactions to select.
        end_date : str
            End date of transactions to select.

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

        #self.data = None

    def __unzip(self, file):
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

    def download_data(self, url):
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
            request = Request(url, None, headers)
            response = urlopen(request)
            return self.__unzip(BytesIO(response.read()))

        except Exception as e:
            logger.error(e)

    def process_resale_data(self, data):
        """
        Select important columns and rows between `start_date` and `end_date`.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        try:
            # select important columns and rows corresponding
            # to successful transactions (`Result` == 'Successful')
            columns = ["loan_id", 'PrincipalAtEnd', 'DiscountRate',
                       'StartDate', 'EndDate']
            data = data.loc[data['Result'] == 'Successful', columns]
            data["loan_id"] = data["loan_id"].apply(lambda s: s[1:-1])
            # convert column type from string to datetime format
            data['StartDate'] = pd.to_datetime(data['StartDate'])
            data['EndDate'] = pd.to_datetime(data['EndDate'])
            # select transactions realized after or on start_date
            if self.start_date:
                data = data.loc[data['EndDate'].dt.date >= self.start_date, :]
            # select transaction realized before or on end_date
            if self.end_date:
                data = data.loc[data['EndDate'].dt.date <= self.end_date, :]
            # remove transactions with `DiscountRate` > 100%
            data = data.loc[data['DiscountRate'] <= 100., :]
            # set `DiscountRate` as integer
            data['DiscountRate'] = data['DiscountRate'].astype(int)
            # calculate time (in seconds) how long a loan was offered for sale
            data['OfferTime'] = (data['EndDate'] - data['StartDate']).astype(
                'timedelta64[s]')
            # remove column `StartDate`
            data.drop('StartDate', axis=1, inplace=True)
            # reset index
            data.reset_index(drop=True, inplace=True)
            return data
        except Exception as e:
            logger.error(e)

    def save_data(self, path, data):
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
        if data is not None:
            with open(path, 'wb') as handle:
                pickle.dump(data,
                            handle,
                            protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    loader = DataLoader("2022-01-01", "2022-12-18")
    #resales = loader.download_data(URL_DATA_RESALES)
    #resales = loader.process_resale_data(resales)
    path_resales = "/resales.pkl"
    #loader.save_data(path_resales, resales)

    #loans = loader.download_data(URL_DATA_LOANS)
    #loans = loader.process_resale_data(loans)
    path_loans = "/loans.pkl"
    #loader.save_data(path_loans, loans)


    resales = pd.read_pickle(path_resales)
    resales = resales.groupby("loan_id", as_index=False). \
        agg(
        tmp1=pd.NamedAgg(column="DiscountRate", aggfunc=max),
        tmp2=pd.NamedAgg(column="DiscountRate", aggfunc=min)
    ). \
        rename(columns={"tmp1": "max_discount",
                        "tmp2": "min_discount"})


    loans = pd.read_pickle(path_loans)
    loan_columns = ["LoanId", "Age", "Country", "Interest", "LoanDuration",
                    "NextPaymentNr", "ProbabilityOfDefault", "Status", "Restructured"]
    loans = loans.loc[:, loan_columns]
    loans = pd.merge(loans, resales, left_on="LoanId", right_on="loan_id", how="inner").\
        drop("loan_id", axis=1)
    loans = loans.loc[(loans["Status"] == "Current") &
                      (~loans["Restructured"]),
                      ["Interest", "NextPaymentNr", "ProbabilityOfDefault",
                       "max_discount", "min_discount"]]
    print(loans.sort_values(by="min_discount"))
