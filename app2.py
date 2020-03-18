import dash, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
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
    dbc.CardHeader("Card portion with options"),
    dbc.CardBody(["Choose the year",
    dcc.Dropdown(
        id="years",
        options=[{"label":i, "value":i} for i in gapm.year],
        value=2002,
        multi=True
    )])
],className="pretty_container"
)

card2 = dbc.Card([
    dbc.CardHeader("Second on the right"),
    dbc.CardBody(
        dcc.Graph(id="plot1")
    )
],
className="pretty_container", color="dark", inverse=True
)

@app.callback(Output("plot1", "figure"),
                     [Input("years", "value")])

def plot1(year_values):

    if type(year_values) != list:
        year_values = [year_values]

    conf_figure = px.scatter(gapm.query("year in @year_values"), 
                            x="gdpPercap", y="lifeExp")

    return conf_figure

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