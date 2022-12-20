"""The file contains the callback definition of web application."""

from dash.dependencies import Input, Output
from pages.dashboard.graphs import create_graph_profit, create_graph_price_distribution


def register_callbacks(app, data):
    """
    Register all callbacks.

    Parameters
    ----------
    app : dash.dash.Dash
        Application where callbacks have to be registered.

    Returns
    -------
    None.

    """

    @app.callback(output=Output("page-content", "children"),
                  inputs=[Input("url", "pathname")])
    def display_page(pathname):
        return layout

    # function to updated initial visible month
    @app.callback(output=Output('date-range', 'initial_visible_month'),
                  inputs=[Input('date-range', 'start_date')])
    def update_initial_visible_month(start_date):
        """
        Set initial visible month of calendar.

        Parameters
        ----------
        start_date : datetime.date
            Date to set as initial visible month of calendar.

        Returns
        -------
        start_date : datetime.date
             Date to set as initial visible month of calendar..

        """
        return start_date

    @app.callback(output=Output("graph_profit", "figure"),
                  inputs=[Input("datepickerrangen_control_1", "start_date"),
                          Input("datepickerrangen_control_1", "end_date"),
                          Input("dropdown_control_2", "value")])
    def update_graph_profit(min_date, max_date, selector):
        min_date = min_date[:10]
        max_date = max_date[:10]
        return create_graph_profit(data[0], min_date, max_date, selector, ["defaulted", "current"])

    @app.callback(output=Output("graph_price_distribution", "figure"),
                  inputs=[Input("datepickerrangen_control_1", "start_date")])
    def update_graph_price_distribution(selector):
        return create_graph_price_distribution(data[1][0], data[1][1], "amount")
