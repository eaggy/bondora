# -*- coding: utf-8 -*-
"""Graphs for this dashboard."""

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from pages.dashboard.columns import ProfitColumns, PriceDistributionColumns
from utils.io import load_transactions
from pages.dashboard.data import transform_data_graph_profit, transform_data_graph_price_distribution


def create_graph_profit(df: pd.DataFrame, min_date: str, max_date: str,
                        selector_time_interval: str, selector_statuses: list) -> go.Figure:
    """Create graph.

    Args:
        df: DaraFrame with data to create graph.
        min_date: Minimal date.
        max_date: Maximal date.
        selector_time_interval: Time interval for the aggregation along the x-axis.
        selector_statuses: State of the loans.

    Returns:
        Graph.

    """
    f_cum_profit = "f_cum_profit"
    pattern_shape_list = ["x", ".", "-", "+", "/", "\\", "|", ""]
    fig = go.Figure()
    idx = 0
    df = df.loc[(df[ProfitColumns.s_selling_date] >= min_date) & (df[ProfitColumns.s_selling_date] <= max_date), :]
    for selector_status in sorted(selector_statuses):
        if len(selector_statuses) == 1:
            pattern_shape = pattern_shape_list[-1]
        else:
            try:
                pattern_shape = pattern_shape_list[idx]
                idx += 1
            except IndexError:
                pattern_shape = pattern_shape_list[-1]
        agg_level = {"d": ProfitColumns.s_selling_date,
                     "m": ProfitColumns.s_selling_month,
                     "y": ProfitColumns.s_selling_year}
        if selector_time_interval in agg_level.keys():
            df_agg = df.loc[df[ProfitColumns.s_loan_status] == selector_status, :].\
                groupby(agg_level[selector_time_interval], as_index=False).\
                agg(tmp1=pd.NamedAgg(column=ProfitColumns.f_profit, aggfunc=sum)).\
                rename(columns={"tmp1": f_cum_profit})
            df_agg.sort_values(by=agg_level[selector_time_interval], inplace=True)
            x = df_agg[agg_level[selector_time_interval]]
            y = df_agg[f_cum_profit]
            color_profit = "green"
            color_loss = "red"
            color = y.apply(lambda v: color_profit if v >= 0. else color_loss)
        else:
            x = []
            y = []
            color = []
        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                name=selector_status,
                marker={"color": color,
                        "pattern_shape": pattern_shape
                        }
            )
        )
    title = "Profit/Loss"
    xaxis_title = "Selling Date"
    yaxis_title = "Profit/loss, €"
    fig.update_layout(title_text=title,
                      barmode="stack",
                      xaxis={"type": "category"},
                      xaxis_title=xaxis_title,
                      yaxis_title=yaxis_title)
    return fig


def create_graph_price_distribution(df_buying: pd.DataFrame, df_selling: pd.DataFrame, dist_type: str) -> go.Figure:
    """Create graph.

        Args:
            df_buying: DaraFrame with buying data to create graph.
            df_selling: DaraFrame with selling data to create graph.
            dist_type: Type of the distribution.

        Returns:
            Graph.

        """
    fig = go.Figure()
    if dist_type == "amount":
        y_buying = df_buying[PriceDistributionColumns.f_bought_amount]
        y_selling = df_selling[PriceDistributionColumns.f_sold_amount]
        yaxis_title = "Amount of transactions, €"
    elif dist_type == "number":
        y_buying = df_buying[PriceDistributionColumns.n_bought_count]
        y_selling = df_selling[PriceDistributionColumns.n_sold_count]
        yaxis_title = "Number of transactions"
    else:
        y_buying = []
        y_selling = []
        yaxis_title = ""
    fig.add_trace(
        go.Bar(
            x=df_buying[PriceDistributionColumns.f_buying_price_percent],
            y=y_buying,
            name="buy",
            marker={"color": "#FF9833",
                    "pattern_shape": ""
                    }
        )
    )
    fig.add_trace(
        go.Bar(
            x=df_selling[PriceDistributionColumns.f_selling_price_percent],
            y=y_selling,
            name="sell",
            marker={"color": "#00CC65",
                    "pattern_shape": ""
                    }
        )
    )
    title = "Buying/Selling Price Distribution"
    xaxis_title = "Price Percentage"
    fig.update_layout(title_text=title,
                      barmode="group",
                      xaxis={"type": "linear"},
                      xaxis_title=xaxis_title,
                      yaxis_title=yaxis_title)
    return fig


if __name__ == "__main__":
    transactions = load_transactions()
    transactions = transform_data_graph_profit(transactions, None)
    graph_profit = create_graph_profit(transactions, "m", ["defaulted", "current"])
    plot(graph_profit)
    #df_buy, df_sell = transform_data_graph_price_distribution(transactions, None)
    #graph_price_distribution = create_graph_price_distribution(df_buy, df_sell, "number")
    #plot(graph_price_distribution)
