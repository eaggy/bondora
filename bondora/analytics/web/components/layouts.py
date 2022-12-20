# -*- coding: utf-8 -*-
"""Layouts of dashboard."""

from typing import List
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.settings import Settings
import plotly.graph_objects as go


class Layout:
    def __init__(self, controls, graphs=[]):
        self.controls = controls
        self.graphs = graphs

    def generate_layout(self, prefix: str = 'main') -> dbc.Container:
        """Generate layout.

        Args:
            prefix: Name used to build IDs. Optional, default is 'main'.

        Returns:
            Layout of main page.

        """
        try:
            figure_graph_profit = self.graphs[0]
        except IndexError:
            figure_graph_profit = go.Figure()
        try:
            figure_graph_price_distribution = self.graphs[1]
        except IndexError:
            figure_graph_price_distribution = go.Figure()
        layout = dbc.Container(
            fluid=True,
            children=[
                # top
                html.H1(
                    Settings.name,
                    id='top'
                ),
                html.Br(),

                # 1st row with inputs
                dbc.Row(
                    children=[
                        dbc.Col(
                            xl=12,
                            children=self.controls[0]

                        )
                    ]
                ),

                # 2nd row with graphs
                dbc.Row(
                    children=[
                        dbc.Col(
                            xl=12,
                            children=[
                                dcc.Graph(
                                    id="graph_profit",
                                    figure=figure_graph_profit
                                )
                            ]
                        )
                    ]
                ),

                # 3rd row with graphs
                dbc.Row(
                    children=[
                        dbc.Col(
                            xl=12,
                            children=[
                                dcc.Graph(
                                    id="graph_price_distribution",
                                    figure=figure_graph_price_distribution
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        return layout
