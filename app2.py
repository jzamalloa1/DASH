import dash, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

## Learnig how to get an infrastructure and ordered app combinind dbc and dcc ##

# DATA
gapm = px.data.gapminder()

# SETTING UP  
stylesheets = [dbc.themes.FLATLY, dbc.themes.GRID]
app = dash.Dash(__name__, external_stylesheets=stylesheets)
app.config["suppress_callback_exceptions"] = True

# APP LAYOUT
card1 = dbc.Card([
    dbc.CardHeader("The title of this"),
    dbc.CardBody("First on the left"),

    dcc.Graph(
        figure = px.scatter(gapm, x="gdpPercap", y="lifeExp")
    )

],className="pretty_container"
)

card2 = dbc.Card(
    "Second on the right", body=True,
    className="pretty_container", color="dark", inverse=True
)

app.layout = html.Div([

    # HEADER PORTION
    html.Div([
        html.Div([
            html.H2("Main Structural View",
                    style={"margin-bottom": "10px"}),
            html.H4("Subtitle")
        ],  
        id="title",
        style ={"width":"100%", "text-align":"center"}
        )
    ],
    id="header",
    style = {"margin-bottom":"25px"}
    ),

    # MAIN BODY
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(card1, width =4),
                dbc.Col(card2, width =8)
            ], no_gutters=True)
        ],
        fluid = True # Container padding
        )
    ],
    id = "first",
    style = {"width":"100%", "margin-left":"0px"}
    )

], 
id="mainContainer",
style = {"display":"flex", "flex-direction":"column"}
)


if __name__== "__main__":
    app.run_server(debug=True)