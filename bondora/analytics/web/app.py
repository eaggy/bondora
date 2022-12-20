# -*- coding: utf-8 -*-
"""The file contains web application."""

import dash
import dash_bootstrap_components as dbc
from components.layouts import Layout
from components.controls import create_controls
from components.settings import Settings
from components.data import get_data
from pages.dashboard.callbacks import register_callbacks


class DashApp(dash.Dash):
    def __init__(self, layout, data, name, title,
                 assets_folder,
                 external_stylesheets, requests_pathname_prefix="/"):
        super().__init__(name=name,
                         title=title,
                         assets_folder=assets_folder,
                         external_stylesheets=external_stylesheets,
                         requests_pathname_prefix=requests_pathname_prefix)
        self.config.suppress_callback_exceptions = True
        self.layout = layout.generate_layout()
        register_callbacks(self, data)


# load data
data = get_data()

# create controls
controls = create_controls(data)

# create layout
layout = Layout(controls)

# create app
app = DashApp(layout=layout,
              data=data,
              name=Settings.name,
              title=Settings.name,
              assets_folder=f"{Settings.root}/assets",
              external_stylesheets=[dbc.themes.LUX])


if __name__ == "__main__":
    app.run_server(debug=Settings.debug,
                   host=Settings.host,
                   port=Settings.port)
else:
    application = app.server
