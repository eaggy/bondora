# -*- coding: utf-8 -*-
"""DataFrame columns."""

from dataclasses import dataclass, astuple


@dataclass(frozen=True)
class PriceDistributionColumns:
    """Dataclass containing names of columns in PriceDistribution."""
    f_bought_amount: str = "f_bought_amount"
    n_bought_count: str = "n_bought_count"
    f_buying_price_percent: str = "f_buying_price_percent"
    s_loan_status: str = "s_loan_status"
    f_selling_price_percent: str = "f_selling_price_percent"
    f_sold_amount: str = "f_sold_amount"
    n_sold_count: str = "n_sold_count"

    @staticmethod
    def get():
        return list(astuple(PriceDistributionColumns()))


@dataclass(frozen=True)
class ProfitColumns:
    """Dataclass containing names of columns in Profit."""
    s_loan_status: str = "s_loan_status"
    f_profit: str = "f_profit"
    s_selling_date: str = "s_selling_date"
    s_selling_month: str = "s_selling_month"
    s_selling_year: str = "s_selling_year"

    @staticmethod
    def get():
        return list(astuple(ProfitColumns()))


@dataclass(frozen=True)
class TransactionsColumns:
    """Dataclass containing names of columns in Transactions."""
    f_amount: str = "Amount"
    ts_buying_date: str = "PurchaseDate"
    f_buying_price: str = "PurchasePrice"
    n_loan_status_code: str = "LoanStatusCode"
    f_principal_repaid: str = "PrincipalRepaid"
    ts_selling_date: str = "SoldDate"
    f_selling_price: str = "SalePrice"

    @staticmethod
    def get():
        return list(astuple(TransactionsColumns()))
