import dash, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
            dbc.Col(
                dcc.Dropdown(id="dynamic_drop",
                    options=[{"label":i, "value":i} for i in set(gapm.continent)],
                    multi=True,
                    placeholder="Select continents",
                    value="Asia"
                ),
                width=3
            )
        ], no_gutters = False, justify="end"),

        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(id="plot1"
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

@app.callback(dash.dependencies.Output("plot1", "figure"),
             [dash.dependencies.Input("dynamic_drop", "value")])

def toggling_figure(conts):
    if  conts is None or len(conts)==0:
        temp_table = gapm
    else:
        temp_table = gapm.query("continent in @conts")

# colorsIdx = {'Moderately Low': 'blue', 'Moderate': 'green', 'Moderately High': 'orange'}

# fig = px.scatter(data, x="1_Yr_Return", y="Expense_Ratio", 
#                  color='Risk', color_discrete_map=colorsIdx)

    cont_figure = px.scatter(temp_table, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                            hover_name="country", log_x=True, size_max=85, 
                            animation_frame="year", animation_group="country",
                            range_x=[np.min(gapm.gdpPercap)-100, np.max(gapm.gdpPercap)+100],
                            range_y=[np.min(gapm.lifeExp)-5, np.max(gapm.lifeExp)+5]
                            ).add_trace(
                                go.Scatter(x=temp_table.gdpPercap, y=temp_table.lifeExp,
                                           name="newish",
                                           mode="markers", marker=dict(size=temp_table["pop"]/10000000))
                            ).update_layout(template = "plotly_dark", height=800, 
                                            transition_duration=3000, transition={"easing":"linear"},
                                            title={"text":"GDP vs Life Expectancy across continents",
                                                    "x":0.5, "xanchor":"center"},
                                            xaxis = {"title":"GDP per Capita"}, 
                                            yaxis = {"title":"Life Expectancy\n(Years)"},
                                            showlegend = True
                            )
                                            


    cont_figure.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
    cont_figure.layout.updatemenus[0].buttons[0].args[1]['frame']['redraw'] = False
    cont_figure.layout.updatemenus[0].buttons[0].args[1]['mode'] = "immediate"

    return cont_figure

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