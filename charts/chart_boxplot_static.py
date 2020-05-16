import plotly.graph_objects as go
import datetime
from plotly import colors


def plot_box_plotly_static(df, column, lands, _colors=colors.diverging.Temps * 3):
    df = df.loc[df.land.isin(lands), ['date','land', column]]  # .sort_values('confirmed_change')
    df.set_index('date', inplace=True, drop=False)
    df_today = df.loc[df.index == df.index.max(), ['land', column]]  # .sort_values('confirmed_change')

    fig = go.Figure()

    for i, l in enumerate(df.land.unique()):
        fig.add_trace(go.Box(
                y=df.loc[df.land == l, column],
                name=l,
                boxpoints='all',  # all, outliers
                jitter=0.5,
                whiskerwidth=0.2,
                # fillcolor=_colors[i],
                marker_color=_colors[i],
                marker_size=2,
                line_width=1)
                     )

    fig.add_trace(go.Scatter(x=df_today['land'],
                         y=df_today[column],
                         mode='markers',
                         name=f"{datetime.datetime.strftime(df_today.index.max(), '%Y-%m-%d')}",
                             marker=dict(
                                     color='#fff',
                                     size=15,
                                     opacity=1,
                                     symbol='star-triangle-up',
                                     line=dict(
                                         # color=_colors[i],
                                         width=1
                                     ))
                         ))

    fig.update_layout(
        # title='',
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=True,
            # dtick=150,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=0,
        ),
        paper_bgcolor="#1f2630",  # "#F4F4F8",
        plot_bgcolor="#1f2630",  # 'white'
        font=dict(color='#2cfec1'),
        autosize=True,
        showlegend=False
    )
    return fig