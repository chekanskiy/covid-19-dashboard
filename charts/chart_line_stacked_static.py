from numpy import log10, seterr
import pandas as pd
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from plotly import colors


def plot_lines_stacked_plotly(
        df,
        column,
        _colors=[
            "#81b2ca",
            "#dea986",
            "#87e7fc",
            "#d3aedf",
            "#93b48f",
            "#a7afe6",
            "#f7fffa",
            "#bba5b5"
        ],
        title=False,
        showlegend=True,
):
    seterr(divide="ignore")

    # Create traces
    fig = go.Figure()

    _labels = df["land"].unique()

    #     max_x_range = len(df.index)
    # _max_y_range = df.loc[df.date == df.date.max(), column].sum() * 1.15
    _max_y_range = df.loc[:, [column]].groupby(by=['date']).sum()[column].max() * 1.1

    if df.loc[:, column].min() > 0:
        _min_y_range = (
                df.loc[(df[column] > 0), column].min() / 2
        )
    else:
        _min_y_range = df.loc[:, column].min() * 1.1

    _symbols = [
        x for i, x in enumerate(SymbolValidator().values) if i % 2 != 0
    ]  # all markers
    _gray_color = "rgb(204, 204, 204)"

    _mode_size = [8] * len(_labels)  # [8, 8, 12, 8]
    _line_size = [1] * len(_labels)  # [2, 2, 4, 2]

    for i, l in enumerate(_labels):
        fig.add_trace(
            go.Scatter(
                x=df.loc[df.land == l].index,
                y=df.loc[df.land == l, column],
                mode="lines",
                name=l,
                line=dict(color=_colors[i], width=_line_size[i]),
                connectgaps=False,
                stackgroup='one'  # define stack group
            )
        )

        # endpoints
        min_index, max_index = (
            df.loc[df.land == l].index.min(),
            df.loc[df.land == l].index.max(),
        )
        fig.add_trace(
            go.Scatter(
                x=[min_index, max_index],
                y=[
                    df.loc[(df.index == min_index) & (df.land == l)],
                    df.loc[(df.index == max_index) & (df.land == l)],
                ],
                mode="markers",
                name=l,
                marker=dict(color=_colors[i], size=_mode_size[i] + 2, ),
                showlegend=False,
            )
        )

    # BUTTONS Changing Y Scale
    updatemenus = list(
        [
            dict(
                active=1,
                direction="left",
                buttons=list(
                    [
                        dict(
                            label="Log",
                            method="update",
                            args=[
                                {"visible": [True, True]},
                                {  # 'title': 'Log scale',
                                    "yaxis": {
                                        "type": "log",
                                        "range": [
                                            log10(_min_y_range),
                                            log10(_max_y_range),
                                        ],
                                        "showgrid": False,
                                        "zeroline": False,
                                        "showline": False,
                                        "linecolor": "#1f2630",
                                    }
                                },
                            ],
                        ),
                        dict(
                            label="Linear",
                            method="update",
                            args=[
                                {"visible": [True, True]},
                                {  # 'title': 'Linear scale',
                                    "yaxis": {
                                        "type": "linear",
                                        "range": [_min_y_range, _max_y_range],
                                        # 'showticklabels': False,
                                        "showgrid": False,
                                        "zeroline": False,
                                        "showline": False,
                                        "linecolor": "#1f2630",
                                    }
                                },
                            ],
                        ),
                    ]
                ),
                type="buttons",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.10,
                xanchor="left",  # ['auto', 'left', 'center', 'right']
                y=1,
                yanchor="top",  # ['auto', 'top', 'middle', 'bottom']
            )
        ]
    )

    # UPDATE LAYOUT, Axis, Margins, Size, Legend, Background
    fig.update_layout(
        updatemenus=updatemenus,
        dragmode="select",
        clickmode="event+select",
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor=_gray_color,
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial", size=12, color="#2cfec1",  # 'rgb(82, 82, 82)',
            ),
            #                 range=[0,max_x_range],
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(color="#2cfec1"),
            range=[_min_y_range, _max_y_range],
        ),
        margin=dict(autoexpand=True, l=10, r=100, t=10, b=100, ),
        showlegend=showlegend,
        legend_orientation="h",
        legend=dict(x=0, y=1.3, ),
        paper_bgcolor="#1f2630",  # "#F4F4F8",
        plot_bgcolor="#1f2630",  # 'white'
        font=dict(color="#2cfec1"),
        autosize=True,
        # width=800,
        # height=500,
    )

    # ANNOTATIONS
    annotations = []

    # Title
    if title:
        annotations.append(
            dict(
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                xanchor="left",
                yanchor="bottom",
                text=title,
                font=dict(
                    family="Garamond", size=30, color="#7fafdf"  # 'rgb(37,37,37)'
                ),
                showarrow=False,
            )
        )

    fig.update_layout(annotations=annotations)

    return fig
