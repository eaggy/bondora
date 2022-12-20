# -*- coding: utf-8 -*-
"""Load and transform data."""

import platform
from typing import List
from utils.io import load_transactions
from pages.dashboard.data import transform_data_graph_price_distribution, transform_data_graph_profit
from pages.dashboard.controls import ControlProfit, ControlPriceDistribution


def get_data() -> List:
    """Load required data.

    Returns:
        Data.

    """
    transactions = load_transactions()

    data = [
        transform_data_graph_profit(transactions, ControlProfit),
        transform_data_graph_price_distribution(transactions, ControlPriceDistribution)
    ]
    return data
