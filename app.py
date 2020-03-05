import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])

# DATA
gapm = px.data.gapminder()

# APP
app.config['suppress_callback_exceptions'] = True

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(id="selected", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("testing",href="/testing", disabled=False),
                dbc.DropdownMenuItem("Page 3", href="/blank"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="My Navigation",
    brand_href="/",
    color="primary",
    dark=True,
    sticky="top"
)

mock_row = dbc.Container(
    [
        dbc.Row(dbc.Col(html.Div("A single column"), width=6), justify="center"), # Grid is of size 12

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), width=True, align="center"), #Default width
                dbc.Col(html.Div("Second of three columns")),
                dbc.Col(html.Div("Third of the three columns!"))
            ],
            no_gutters = False, justify="center"
        )
    ],
    fluid=False # If False, container padding is on
)

mock_graphs = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(
                    figure = px.scatter(gapm, x="gdpPercap", y="lifeExp")
                             .update_layout(template = "plotly_white")
                )
            ]), width=4),

            dbc.Col(html.Div([
                dcc.Graph(
                    figure = px.scatter(gapm, x="gdpPercap", y="lifeExp", color="continent")
                )
            ]), width=4),

            dbc.Col(html.Div([
                dcc.Graph(
                    figure = px.scatter(gapm, x="gdpPercap", y="lifeExp", color="continent", size="pop",
                                        log_x=True)
                )
            ]), width=4)
        ],
        no_gutters = True, justify="center"
        ),

        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(
                    figure = px.scatter(gapm, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                                        hover_name="country", log_x=True, animation_frame="year", animation_group="country",
                                        range_x=[np.min(gapm.gdpPercap)-100, np.max(gapm.gdpPercap)+100],
                                        range_y=[np.min(gapm.lifeExp)-1, np.max(gapm.lifeExp)+1]
                                        )
                                        .update_layout(template = "plotly_dark", height=800,
                                                       transition = {'duration': 5000}
                                                      )
                )
            ]), width=12)
        ])
    ],
    fluid=True
)

index_page = html.Div([navbar, mock_graphs])

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@app.callback(dash.dependencies.Output("page-content", "children"),
              [dash.dependencies.Input("url", "pathname")]
              )

def display_page(pathname):
    if pathname == "/testing":
        return html.Div([navbar, mock_row])
    elif pathname== "/blank":
        return html.Div([navbar, html.H1("Blank page")])
    else:
        return index_page


@app.callback(dash.dependencies.Output("selected", "children"),
             [dash.dependencies.Input("url", "pathname")]
             )

def selected_name(pathname):
    if pathname=="/":
        return html.H5("Main summary")
    else:
        pathname = pathname.lstrip("/")
    return pathname



if __name__ == "__main__":
    app.run_server(debug=True)