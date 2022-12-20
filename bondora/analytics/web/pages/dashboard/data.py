# -*- coding: utf-8 -*-
"""Data transformer for this dashboard."""

import pandas as pd
from typing import Tuple
from dataclasses import dataclass
from utils.io import load_transactions
from pages.dashboard.columns import PriceDistributionColumns, ProfitColumns, TransactionsColumns


def transform_data_graph_price_distribution(df_transact: pd.DataFrame,
                                            control: dataclass) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Transform data for this graph.

        Args:
            df_transact: DataFrame with transactions.

        Returns:
            DataFrames with prepared data.

        """
    #pd.set_option('display.max_rows', 100)
    #pd.set_option('display.max_columns', 100)
    # calculate prices in percentage
    df_transact[PriceDistributionColumns.f_buying_price_percent] = 100. * (
            (df_transact[TransactionsColumns.f_buying_price] -
             df_transact[TransactionsColumns.f_amount] +
             0. * df_transact[TransactionsColumns.f_principal_repaid]) /
            (df_transact[TransactionsColumns.f_amount] - 0. * df_transact[TransactionsColumns.f_principal_repaid])
    )
    df_transact[PriceDistributionColumns.f_buying_price_percent] = \
        df_transact[PriceDistributionColumns.f_buying_price_percent].\
        apply(lambda x: round(x) if x < 100. else x).astype(float)
    df_transact[PriceDistributionColumns.f_selling_price_percent] = 100. * (
            (df_transact[TransactionsColumns.f_selling_price] -
             df_transact[TransactionsColumns.f_amount] +
             0. * df_transact[TransactionsColumns.f_principal_repaid]) /
            (df_transact[TransactionsColumns.f_amount] - 0. * df_transact[TransactionsColumns.f_principal_repaid])
    )
    df_transact[PriceDistributionColumns.f_selling_price_percent] = \
        df_transact[PriceDistributionColumns.f_selling_price_percent].\
        apply(lambda x: round(x) if x < 100. else x).astype(float)
    # map loan status code
    mapping = {2: "current",
               5: "defaulted",
               100: "defaulted"}
    df_transact[PriceDistributionColumns.s_loan_status] = df_transact[TransactionsColumns.n_loan_status_code].\
        map(mapping)
    df_transact.dropna(subset=PriceDistributionColumns.s_loan_status, inplace=True)
    df_selected = df_transact.loc[df_transact[PriceDistributionColumns.s_loan_status].isin(mapping.values()), :]
    df_agg_buying = df_selected.groupby(PriceDistributionColumns.f_buying_price_percent, as_index=False). \
        agg(
        tmp1=pd.NamedAgg(column=TransactionsColumns.f_buying_price, aggfunc=sum),
        tmp2=pd.NamedAgg(column=TransactionsColumns.f_buying_price, aggfunc=len)
    ). \
        rename(columns={"tmp1": PriceDistributionColumns.f_bought_amount,
                        "tmp2": PriceDistributionColumns.n_bought_count})
    df_agg_selling = df_selected.groupby(PriceDistributionColumns.f_selling_price_percent, as_index=False). \
        agg(
        tmp1=pd.NamedAgg(column=TransactionsColumns.f_selling_price, aggfunc=sum),
        tmp2=pd.NamedAgg(column=TransactionsColumns.f_selling_price, aggfunc=len)
    ). \
        rename(columns={"tmp1": PriceDistributionColumns.f_sold_amount,
                        "tmp2": PriceDistributionColumns.n_sold_count})
    return df_agg_buying, df_agg_selling


def transform_data_graph_profit(df_transact: pd.DataFrame, control: dataclass) -> pd.DataFrame:
    """Transform data for this graph.

        Args:
            df_transact: DataFrame with transactions.

        Returns:
            DataFrame with prepared data.

        """
    # calculate profit
    df_transact[ProfitColumns.f_profit] = (df_transact[TransactionsColumns.f_selling_price] -
                                           df_transact[TransactionsColumns.f_buying_price] +
                                           df_transact[TransactionsColumns.f_principal_repaid])
    # add data columns
    df_transact[ProfitColumns.s_selling_date] = df_transact[TransactionsColumns.ts_selling_date].apply(lambda d: d[:10])
    df_transact[ProfitColumns.s_selling_month] = df_transact[TransactionsColumns.ts_selling_date].apply(lambda d: d[:7])
    df_transact[ProfitColumns.s_selling_year] = df_transact[TransactionsColumns.ts_selling_date].apply(lambda d: d[:4])
    # map loan status code
    mapping = {2: "current",
               5: "defaulted",
               100: "defaulted"}
    df_transact[ProfitColumns.s_loan_status] = df_transact[TransactionsColumns.n_loan_status_code].map(mapping)
    df_transact.dropna(subset=ProfitColumns.s_loan_status, inplace=True)
    df_transact = df_transact[ProfitColumns.get()]
    return df_transact
