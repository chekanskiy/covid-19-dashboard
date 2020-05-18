import pandas as pd
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly import colors

from dash.dependencies import Input, Output, State

# APP_PATH = str(pathlib.Path(__file__).parent.resolve())
# sys.path.insert(0, APP_PATH)

from charts.chart_choropleth import plot_map_go
from charts.chart_boxplot_static import plot_box_plotly_static
from charts.chart_line_static import plot_lines_plotly
from charts.chart_sunburst_static import plot_sunburst_static
from charts.chart_bar_static import plot_bar_static

# ============================================ LOAD DATA =====================================================
df_rki_orig = pd.read_csv('data/data_rki_apple_prepared_dash.csv')
df_jh_world = pd.read_csv('data/data_jhu_world.csv')
df_jh_world.loc[:, 'population_100k'] = df_jh_world.loc[:, 'population_wb'] / 100000
df_jh_world['date'] = df_jh_world['date'].astype('datetime64[ns]')

df_rki_orig['date'] = df_rki_orig['date'].astype('datetime64[ns]')
geojson = json.load(open('data/data_geo_de.json', 'r'))
# ========================================= END LOAD DATA ====================================================

# ========================================= CREATE APP =======================================================
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],)
# external_stylesheets=external_stylesheets)
server = app.server

# ========================================= DEFINE PROPERTIES ================================================
STATES = {'BW': 'Baden-Wuerttemberg',
          'BY': 'Bavaria',
          'BE': 'Berlin',
          'BB': 'Brandenburg',
          'HB': 'Bremen',
          'HH': 'Hamburg',
          'HE': 'Hesse',
          'NI': 'Lower Saxony',
          'MV': 'Mecklenburg-Western Pomerania',
          'NW': 'North Rhine-Westphalia',
          'RP': 'Rhineland-Palatinate',
          'SL': 'Saarland',
          'SN': 'Saxony',
          'ST': 'Saxony-Anhalt',
          'SH': 'Schleswig-Holstein',
          'TH': 'Thuringia'}

COLORS = {
    'background': '#1f2630',
    'text': '#2cfec1',
    # 'charts': colors.diverging.Temps * 3
    'charts': colors.diverging.Tealrose * 3,  # 'YlGnBu',
    'map': colors.sequential.PuBu  # 'YlGnBu',
}

BASE_FIGURE = dict(
                data=[dict(x=0, y=0)],
                layout=dict(
                    paper_bgcolor=COLORS['background'],
                    plot_bgcolor=COLORS['background'],
                    autofill=True,
                    margin=dict(t=75, r=50, b=100, l=50),
                            ),
                    )

FEATURE_DROP_DOWN = {
    "confirmed_change": "Cases: Daily",
    "confirmed": "Cases: Total",
    "confirmed_active_cases": "Cases: Active",
    "confirmed_per_100k": "Cases: Total per 100k of Population",
    "confirmed_change_per_100k": "Cases: Daily per 100k of Population",
    "confirmed_change_pct_3w": "Cases: Daily as % of Rolling 3 Week Sum",
    "confirmed_doubling_days_3w_avg3": "Cases: Days to Double Rolling 3 Week Sum",
    "dead_change": "Deaths: Daily",
    "dead": "Deaths: Total",
    "dead_per_100k": "Dead: Total per 100k of Population",
    "dead_change_per_100k": "Deaths: Daily per 100k of Population",
    "dead_doubling_days": "Deaths: Days to Double Total Number",
    "driving": "Driving traffic relative to January 2020",
    "walking": "Walking traffic relative to January 2020",
    "transit": "Transit traffic relative to January 2020",
}

TABS_STYLES = {
    'height': '6rem',
    'borderBottom': '0px solid #7fafdf',
    'padding': '0 0 0 0',
}

TAB_STYLE = {
    'borderTop': '0px solid #7fafdf',
    'borderLeft': '0px solid #7fafdf',
    'borderRight': '0px solid #7fafdf',
    'borderBottom': '0px solid #7fafdf',
    'backgroundColor': '#252e3f',
    'color': "while",
    'textAlign': 'center',
    'fontSize': '14px',
    'fontWeight': 'bold',
    'padding': '2rem 0 0 0',
}

TAB_SELECTED_STYLE = {
    'borderTop': '0px solid #7fafdf',
    'borderLeft': '0px solid #7fafdf',
    'borderRight': '0px solid #7fafdf',
    'borderBottom': '0px solid #7fafdf',
    'backgroundColor': COLORS['background'],
    'color': 'white',
    'textAlign': 'center',
    'fontSize': '14px',
    'fontWeight': 'bold',
    'padding': '2rem 0 0 0',
}

# ========================================= DEFINE LAYOUT ================================================
app.layout = html.Div(
    id="root",
    # style={'backgroundColor': colors['background']},
    children=[
        html.Div(
            id='header',
            children=[
                # html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                html.H4(children='COVID-19 in Germany', #style={ 'textAlign': 'left', 'color': colors['text']}
                        ),
                html.P(
                      id="description",
                      children="Fully interactive dashboard",
                  ),
                    ]
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="dropdown-container",
                            children=[
                                html.P(
                                    id="dropdown-text",
                                    children="Select states below or circle states on the map",
                                ),
                                html.Div(
                                    dcc.Dropdown(
                                        id="dropdown-states",
                                        multi=True,
                                        value=['Hamburg', 'Bremen', 'Berlin'],  # Or single value, like Hamburg
                                        options=[
                                                {
                                                 "label": str(iso),
                                                 "value": str(state),
                                                }
                                                for state, iso in zip(STATES.values(), STATES.keys())],
                                                    ),
                                    style={'width': '100%', 'display': 'inline-block',
                                           }
                                        ),
                                # html.Div(dcc.DatePickerRange(
                                #     id='date-picker-range',
                                #     start_date=dt(1997, 5, 3),
                                #     end_date_placeholder_text='Select a date!',
                                # ),
                                #     style={'width': '15%', 'display': 'inline-block', 'margin-left': 10,
                                #            'background-color': 'inherit',
                                #            'virticalalign': 'middle'})
                            ],
                        ),
                        html.Div(
                            id="left-chart-container",
                            children=[
                                html.Div(children=[
                                    html.Div(
                                        id='div-button-weekly-top',
                                        className='div-button-weekly-average',
                                        children=dbc.Button(
                                                            children="7 Day Avg Off/On",
                                                            id='button-weekly-top', size='sm', color="info"),
                                        style={'display': 'inline-block'}),
                                    html.Div(html.P(
                                        id="left-chart-title",),
                                        style={'display': 'inline-block',}
                                            ),
                                                ],
                                        ),
                                dcc.Graph(
                                    id='left-chart',
                                    figure=BASE_FIGURE
                                         ),
                                html.Div(children=[
                                    html.Div(
                                        id='div-button-weekly-mobility',
                                        className='div-button-weekly-average',
                                        children=dbc.Button(children="7 Day Avg Off/On",
                                                            id='button-weekly-mobility', size='sm', color="info"),
                                        style={'display': 'inline-block'}),
                                    html.Div(html.P(
                                        children="Driving traffic relative to January 2020",
                                        id="left-chart-2-title", ),
                                        style={'display': 'inline-block',
                                               'margin-right': 0, 'margin-left': 0,
                                               }),
                                ],
                                ),
                                dcc.Graph(
                                    id='left-chart-2',
                                    figure=BASE_FIGURE
                                         ),
                                # dcc.Loading(
                                #     id="loading-1",
                                #     type="circle",
                                #     children=[
                                #
                                #             ])
                            ])
                            ]
                        ),
                html.Div(
                    id="right-column",
                    children=[
                        html.Div(
                            id='dropdown-and-tab-container',
                            children=[
                                html.P(id="chart-selector", children="Select the value to plot:"),
                                dcc.Dropdown(
                                    options=[{'label': l, 'value': v} for l, v in
                                             zip(FEATURE_DROP_DOWN.values(), FEATURE_DROP_DOWN.keys())],
                                    value="confirmed_change",
                                    id="chart-dropdown",
                                ),
                                dcc.Tabs(id='tabs-example',
                                         parent_className='custom-tabs',
                                         className='custom-tabs-container',
                                         value='tab-map',
                                         children=[
                                            dcc.Tab(label='Map Tab', value='tab-map',
                                                    style=TAB_STYLE,
                                                    selected_style=TAB_SELECTED_STYLE
                                                    ),
                                            dcc.Tab(label='Boxplot Tab', value='tab-boxplot',
                                                    style=TAB_STYLE,
                                                    selected_style=TAB_SELECTED_STYLE
                                                    ),
                                                    ], style=TABS_STYLES),
                                ]),
                        html.Div(
                            id='right-chart-container',
                            children=[
                                html.Div(children=[
                                    dcc.Graph(
                                        id="right-chart",
                                        figure=BASE_FIGURE,
                                            ),],
                                ),
                                html.Div(html.P(
                                    children=' ',
                                    id="right-chart-2-title", ),
                                    style={'display': 'inline-block', }
                                ),
                                html.Div(children=[dcc.Graph(
                                    id="right-chart-2",
                                    figure=BASE_FIGURE, )],
                                        )
                        ]),
                            ],
                        )
                ]
                    )
    ])


@app.callback(
    Output("button-weekly-top", "children"),
    [Input("button-weekly-top", "n_clicks")])
def update_weekly_button(n_clicks):
    """
    Changes the name displayed on the button button-weekly-top
    based on how many times it was clicked (even / uneven number of times)
    :param n_clicks:
    :return:
    """
    if n_clicks is None or n_clicks % 2 == 0:
        return "7 DAY AVG IS ON"
    else:
        return "7 DAY AVG IS OFF"


@app.callback(
    Output("button-weekly-mobility", "children"),
    [Input("button-weekly-mobility", "n_clicks")])
def update_weekly_button(n_clicks):
    """
    Changes the name displayed on the button button-weekly-left-chart-2
    based on how many times it was clicked (even / uneven number of times)
    :param n_clicks:
    :return:
    """
    if n_clicks is None or n_clicks % 2 == 0:
        return "7 DAY AVG IS OFF"
    else:
        return "7 DAY AVG IS ON"


def moving_average_7d(df, selected_column):
    """
    Adds a column to the df with the 7days moving average of the selected column for
    each 'land' individually
    :param df:
    :param selected_column:
    :return:
    """
    ro = df.groupby('land').rolling(7, on='date').mean().reset_index(drop=False).loc[:,
         ['date', 'land', selected_column]]
    df = df.merge(ro, on=['date', 'land'], suffixes=('', '_weekly')).round(3)
    selected_column += '_weekly'
    return df, selected_column


@app.callback(
    Output('left-chart', 'figure'),
    [Input('chart-dropdown', 'value'),
     Input('dropdown-states', 'value'),
     Input("button-weekly-top", "n_clicks")
    ])
def update_left_chart(selected_column, selected_states, n_clicks):
    """
    Displays / Updates the left chart.
    Number of clicks on the button-weekly-top object define how the data is filtered
    :param selected_column:
    :param selected_states:
    :param n_clicks:
    :return:
    """
    if len(selected_states) > 0:  # In case all states are deselected
        if n_clicks is None or n_clicks % 2 == 0:  # Button is Un-clicked or Clicked even number of times.
            df, selected_column = moving_average_7d(df_rki_orig, selected_column)
        else:
            df = df_rki_orig

        figure = plot_lines_plotly(df, selected_states, selected_column,
                                   show_doubling=True, doubling_days=7, showlegend=False,
                                   _colors=COLORS['charts'])
    else:  # Default figure is displayed initially, on refresh and when no states are selected
        figure = BASE_FIGURE
    return figure


@app.callback(
    Output('left-chart-2', 'figure'),
    [Input('dropdown-states', 'value'),
     Input("button-weekly-mobility", "n_clicks")
    ])
def update_left_chart_2(selected_states, n_clicks):
    """
    Displays / Updates the left chart.
    Number of clicks on the button-weekly-mobility object define how the data is filtered
    No averaging by default
    :param selected_column:
    :param selected_states:
    :param n_clicks:
    :return:
    """
    if len(selected_states) > 0:  # In case all states are deselected
        columns_mobility = ['driving', 'walking', 'transit']
        selected_column = columns_mobility[0]

        if n_clicks is None or n_clicks % 2 == 0:  # Button is Un-clicked or Clicked even number of times.
            df = df_rki_orig
        else:
            df, selected_column = moving_average_7d(df_rki_orig, selected_column)

        figure = plot_lines_plotly(df, selected_states, selected_column,
                                   show_doubling=False, doubling_days=7, showlegend=False,
                                   _colors=COLORS['charts'])
    else:  # Default figure is displayed initially, on refresh and when no states are selected
        figure = BASE_FIGURE
    return figure


def update_right_chart_map(selected_column, selected_date='most_recent'):
    """
    Helper function that filters the data for the Map Chart
    :param selected_column:
    :param selected_date:
    :return: figure
    """
    df = df_rki_orig.loc[:, [selected_column, 'land', 'iso_code', 'date']].set_index('date', drop=False)
    if selected_date == 'most_recent':
        df = df.loc[df.index == df.index.max()]
    else:
        df = df.loc[df.index == selected_date]
    figure = plot_map_go(df, geojson, selected_column, _colors=COLORS['map'])
    return figure


@app.callback(
    Output('right-chart', 'figure'),
    [Input('chart-dropdown', 'value'),
     Input('dropdown-states', 'value'),
     Input('tabs-example', 'value'),
     Input('left-chart', 'selectedData')],
)
def update_right_chart(selected_column, selected_states, selected_tab, selected_data):
    """
    Displays / Updates the chart on the right based on input.
    Changing any value redraws the chart.
    This is why the country selection on the map doesn't persist (the chart updates)
    :param selected_column:
    :param selected_states:
    :param selected_tab:
    :param selected_data:
    :return:
    """
    if selected_tab == 'tab-boxplot':
        if len(selected_states) > 0:
            figure = plot_box_plotly_static(df_rki_orig, selected_column, selected_states)
        else:
            figure = BASE_FIGURE
        return figure
    if selected_tab == 'tab-map':
        if selected_data is None:
            selected_date = 'most_recent'
        else:
            selected_date = selected_data['points'][-1]['x']
        return update_right_chart_map(selected_column, selected_date)


def select_value_for_boxplot(selected_column):
    if selected_column in ('driving', 'walking', 'transit'):
        selected_column = 'confirmed_change'
    return selected_column


@app.callback(
    Output('right-chart-2', 'figure'),
    [Input('chart-dropdown', 'value'),
     Input('dropdown-states', 'value'),
     Input('left-chart', 'selectedData')],
)
def update_right_chart_2(selected_column, selected_states, selected_data):
    """
    Displays / Updates the chart on the right based on input.
    Changing any value redraws the chart.
    This is why the country selection on the map doesn't persist (the chart updates)
    :param selected_column:
    :param selected_states:
    :param selected_tab:
    :param selected_data:
    :return:
    """
    selected_column = select_value_for_boxplot(selected_column)

    if len(selected_states) > 0:
        df_jh_world.index = df_jh_world.date
        df = df_jh_world.loc[df_jh_world.index == df_jh_world.index.max()]
        if '100k' in selected_column or selected_column in \
                ('confirmed_change_pct_3w', 'confirmed_doubling_days_3w_avg3',
                 'dead_change_pct_3w', 'dead_doubling_days_3w_avg3'):
            if 'doubling_days' in selected_column:
                df = df.loc[df[selected_column] > 0].sort_values(selected_column, ascending=True).head(25)
            else:
                df = df.sort_values(selected_column, ascending=False).head(25)
            figure = plot_bar_static(df, selected_column)
        else:
            figure = plot_sunburst_static(df, selected_column,
                                          color_columns=[selected_column, 'population_100k'],
                                          value_column_name=FEATURE_DROP_DOWN[selected_column])
    else:
        figure = BASE_FIGURE
    return figure


@app.callback(
    Output('right-chart-2-title', 'children'),
    [Input('chart-dropdown', 'value'),
    ])
def update_right_chart_2_title(selected_column):
    """
    Updates the Title of the left chart based on  the value selected in the right drop-down menu and
    the state of the button selecting averaging
    :param selected_column:
    :param n_clicks:
    :return: string: Title to display
    """
    selected_column = select_value_for_boxplot(selected_column)

    return "Global " + FEATURE_DROP_DOWN[selected_column]


@app.callback(
    Output('left-chart-title', 'children'),
    [Input('chart-dropdown', 'value'),
     Input("button-weekly-top", "n_clicks")
    ])
def update_left_chart_title(selected_column, n_clicks):
    """
    Updates the Title of the left chart based on  the value selected in the right drop-down menu and
    the state of the button selecting averaging
    :param selected_column:
    :param n_clicks:
    :return: string: Title to display
    """
    if n_clicks is None or n_clicks % 2 == 0:  # Button is Un-clicked or Clicked even number of times.
        return FEATURE_DROP_DOWN[selected_column] + ', 7 day moving average'
    else:
        return FEATURE_DROP_DOWN[selected_column] + ', by day'


# @app.callback(
#     Output('left-chart-title', 'children'),
#     [Input('left-chart', 'selectedData')
#     ])
# def test_update_left_chart_title(data):
#     """
#     Test Callback to print values returned by selectedData object.
#     Keep it commented out if not debugging.
#     :param data:
#     :return:
#     """
#     return str(data['points'][0]['x'])


@app.callback(
    Output('dropdown-states', 'value'),
    [Input('right-chart', 'selectedData'),],
    [State('dropdown-states', 'value')])
def update_states_selection_from_map(selected_data, drop_down_states):
    """
    Selecting the data on the Map Chart updates the values in the
    Dropdown Menu on the left
    :param selected_data:
    :param drop_down_states:
    :return: list of values for the Dropdown Menu
    """
    if selected_data is None:
        return drop_down_states
    else:
        return [str(p['text']) for p in selected_data['points']]


if __name__ == '__main__':
    app.run_server(debug=True)