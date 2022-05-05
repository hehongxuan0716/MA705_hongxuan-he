import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

stylesheet = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=stylesheet)

df = pd.read_csv("michelin_my_maps.csv")

fig1 = px.pie(df, "Award", title="Michelin Restaurant Awards")

app.layout = html.Div(
    [
        html.H1("Michelin Guide Restaurants 2021"),
        html.Blockquote("Individual MA705 Project | Hongxuan He"),
        html.Div(
            [
                html.H2("Context"),
                html.P(
                    "At the beginning of the automobile era, Michelin, a tire company, created a travel guide, including a restaurant guide."
                ),
                html.P(
                    "Through the years, Michelin stars have become very prestigious due to their high standards and very strict anonymous testers. Michelin Stars are incredibly coveted. Gaining just one can change a chef's life; losing one, however, can change it as well."
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Content"),
                        html.P(
                            "The dataset contains a list of restaurants along with additional details (e.g. address, price range, cuisine type, longitude, latitude, etc.) curated from the MICHELIN Restaurants guide. The culinary distinctions (i.e. the 'Award' column) of the restaurants included are:"
                        ),
                        html.Li("3 Stars"),
                        html.Li("2 Stars"),
                        html.Li("1 Stars"),
                        html.Li("Bib Gourmand"),
                    ],
                    className="six columns",
                ),
                dcc.Graph(
                    figure=fig1,
                    className="six columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Parameters"),
                        html.P("Select a Award:"),
                        dcc.Checklist(
                            [
                                "1 MICHELIN Star",
                                "2 MICHELIN Stars",
                                "3 MICHELIN Stars",
                                "Bib Gourmand",
                            ],
                            [
                                "1 MICHELIN Star",
                                "2 MICHELIN Stars",
                                "3 MICHELIN Stars",
                                "Bib Gourmand",
                            ],
                            id="award",
                        ),
                        html.Br(),
                        html.P("Select a Currency:"),
                        dcc.Dropdown(
                            df.Currency.unique(),
                            multi=True,
                            id="currency",
                        ),
                        html.Br(),
                        html.P("Select a Cuisine:"),
                        dcc.Dropdown(
                            list(
                                set(
                                    sum(
                                        df.Cuisine.apply(
                                            lambda x: [i.strip() for i in x.split(",")]
                                        ).values,
                                        [],
                                    )
                                )
                            ),
                            id="cuisine",
                        ),
                    ],
                    className="four columns",
                ),
                dcc.Graph(
                    className="eight columns",
                    id="graph",
                ),
            ],
            className="row",
        ),
        dash_table.DataTable(
            df.to_dict("records"),
            [{"name": i, "id": i} for i in df.columns],
            page_size=10,
            fixed_columns={"headers": True, "data": 1},
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            style_table={"minWidth": "100%"},
            style_cell={
                "maxWidth": "200px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
            id="table",
        ),
        html.Div(
            [
                html.H2("References"),
                html.P(
                    "Here is a list of data sources and references used in this course project."
                ),
                html.Li(
                    [
                        "Explore the world of the MICHELIN Guide: ",
                        html.A(
                            "https://guide.michelin.com/en",
                            href="https://guide.michelin.com/en",
                        ),
                    ]
                ),
                html.Li(
                    [
                        "Dash DataTable: ",
                        html.A(
                            "https://dash.plotly.com/datatable",
                            href="https://dash.plotly.com/datatable",
                        ),
                    ]
                ),
                html.Li(
                    [
                        "Dash Plotly Pie Chart: ",
                        html.A(
                            "https://plotly.com/python/pie-charts/",
                            href="https://plotly.com/python/pie-charts/",
                        ),
                    ]
                ),
                html.Li(
                    [
                        "Dash Plotly Callbacks: ",
                        html.A(
                            "https://dash.plotly.com/datatable/callbacks",
                            href="https://dash.plotly.com/datatable/callbacks",
                        ),
                    ]
                ),
            ]
        ),
        html.Br(),
        html.P("May 2022, Hongxuan He"),
    ],
    style={"margin": "50px 5%"},
)

server = app.server


@app.callback(
    Output(component_id="table", component_property="data"),
    [
        Input(component_id="award", component_property="value"),
        Input(component_id="currency", component_property="value"),
        Input(component_id="cuisine", component_property="value"),
    ],
)
def update_table(award, currency, cuisine):
    x = df[df.Award.isin(award)]
    if currency:
        x = x[x.Currency.isin(currency)]
    if cuisine:
        x = x[df.Cuisine.str.contains(cuisine)]
    return x.to_dict("records")


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [
        Input(component_id="award", component_property="value"),
        Input(component_id="currency", component_property="value"),
        Input(component_id="cuisine", component_property="value"),
    ],
)
def update_gragh(award, currency, cuisine):
    x = df[df.Award.isin(award)]
    if currency:
        x = x[x.Currency.isin(currency)]
    if cuisine:
        x = x[df.Cuisine.str.contains(cuisine)]
    return px.pie(
        x,
        "Award",
        title=f"There are {x.shape[0]} Michelin Restaurants that match your search.",
    )


if __name__ == "__main__":
    app.run_server()
