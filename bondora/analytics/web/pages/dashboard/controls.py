# -*- coding: utf-8 -*-
"""Control elements of this dashboard."""

from dataclasses import dataclass

import pandas as pd
from dash import html, dcc
from typing import Tuple
import dash_bootstrap_components as dbc
from dataclasses import dataclass
from pages.dashboard.columns import ProfitColumns


@dataclass(frozen=True)
class ControlPriceDistribution:
    """Dataclass containing names of control elements."""
    selector1: str = "tmp"


@dataclass(frozen=True)
class ControlProfit:
    """Dataclass containing names of control elements."""
    selector1: str = "tmp"


def create_control(df: pd.DataFrame) -> dbc.Row:
    """Create control elements of this dashboard.

    Args:
        df: DataFrame with data to create control element.

    Returns:
        Row with control elements.

    """
    from datetime import datetime, timedelta
    min_date = min(df[ProfitColumns.s_selling_date].values)
    max_date = max(df[ProfitColumns.s_selling_date].values)



    control = html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H5('Select Date Range'),
                            dcc.DatePickerRange(
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                initial_visible_month=max_date,
                                start_date=min_date,
                                end_date=max_date,
                                display_format="DD.MM.YYYY",
                                id="datepickerrangen_control_1"
                            )
                        ],
                        id="col_control_1",
                        width=9
                    )
                ],
                id="row_control_1",
                style={"marginTop": "0px",
                       "marginBottom": "20px"}
            ),

            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.H5("Select Time Resolution"),
                            dcc.Dropdown(
                                options=[{"label": "day", "value": "d"},
                                         {"label": "month", "value": "m"},
                                         {"label": "year", "value": "y"}],
                                value="d",
                                multi=False,
                                searchable=False,
                                clearable=False,
                                id="dropdown_control_2",
                                className="dropdown"
                            )
                        ],
                        id="col_control_2",
                        width=9
                    )
                ],
                id="row_control_2",
                style={"marginTop": "0px",
                       "marginBottom": "20px"}
            )
        ]
    )
    return control
