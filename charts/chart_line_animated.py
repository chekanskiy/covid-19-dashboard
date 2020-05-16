import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator


def plot_lines_plotly_animated(df, title, show_doubling=True, doubling_days=7, showlegend=False):
    doubling_column = f'double_x{doubling_days}'
    if show_doubling:
        def double_every_x_days(day, days_doubling):
            r = 1 * 2 ** (day / days_doubling)
            return r

        df['day'] = df.index
        df[doubling_column] = df['day'].apply(lambda x: double_every_x_days(x, doubling_days))
        del df['day']

    # Create traces
    fig = go.Figure()

    labels = [c for c in df.columns if c != doubling_column]
    max_y_range = int(max(df.loc[:, labels].max()) * 1.1)
    #     max_x_range = len(df.index)
    colors = plotly.colors.diverging.Temps + plotly.colors.diverging.Temps  # 10 colors #['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
    symbols = [x for i, x in enumerate(SymbolValidator().values) if i % 2 != 0]  # all markers
    gray_color = 'rgb(204, 204, 204)'
    days = df.index
    animation_speed = 50

    mode_size = [8] * len(df.columns)  # [8, 8, 12, 8]
    line_size = [1] * len(df.columns)  # [2, 2, 4, 2]

    for i, col in enumerate(df.columns):
        # Adding Doubling x7 line
        if col == doubling_column:
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[col],
                                     mode='lines',
                                     marker=dict(color=gray_color,
                                                 size=mode_size[i] - 2,
                                                 opacity=0.7,
                                                 symbol=symbols[i + 2],
                                                 line=dict(
                                                     color=colors[i],
                                                     width=1
                                                 )
                                                 ),
                                     name=col,
                                     line=dict(color=gray_color,
                                               width=line_size[i],
                                               dash='dot', ),
                                     connectgaps=True,
                                     ))

        # Adding all other lines
        else:
            fig.add_trace(go.Scatter(x=df.index,
                                     y=df[col],
                                     mode='lines+markers',
                                     marker=dict(color=colors[i],
                                                 size=mode_size[i] - 3,
                                                 opacity=0.7,
                                                 symbol=symbols[i + 2],
                                                 line=dict(
                                                     color=colors[i],
                                                     width=1
                                                 )
                                                 ),
                                     name=col,
                                     line=dict(color=colors[i],
                                               width=line_size[i]),
                                     connectgaps=False,
                                     ))

    # BUTTONS Changing Y Scale
    updatemenus = list([
        dict(active=1,
             buttons=list([
                 dict(label='Scale: Log',
                      method='update',
                      args=[{'visible': [True, True]},
                            {'title': 'Log scale',
                             'yaxis': {'type': 'log', 'range': [0, np.log10(max_y_range)],
                                       'showgrid':False,
                                       'zeroline':False,
                                       'showline':False,
                                       'linecolor': '#1f2630',
                                      }}
                            ]
                      ),
                 dict(label='Scale: Linear',
                      method='update',
                      args=[{'visible': [True, True]},
                            {'title': 'Linear scale',
                             'yaxis': {'type': 'linear', 'range': [0, max_y_range],
                                       # 'showticklabels': False,
                                       'showgrid':False,
                                       'zeroline':False,
                                       'showline':False,
                                       'linecolor':'#1f2630',
                                       }}
                            ]
                      ),
                 dict(label='Play',
                      method='animate',
                      args=[None, {"frame": {"duration": animation_speed, "redraw": False},
                                   "fromcurrent": True, "transition": {"duration": animation_speed * 0.8,
                                                                       "easing": "quadratic-in-out"}}
                            ]
                      ),
                 dict(
                     args=[[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                     label="Pause",
                     method="animate"
                 )
             ]),
             type='buttons',
             pad={"r": 10, "t": 10},
             showactive=True,
             x=-0.15,
             xanchor="left",  # ['auto', 'left', 'center', 'right']
             y=0.35,
             yanchor='bottom',  # ['auto', 'top', 'middle', 'bottom']
             )
    ])

    # ===== SLIDER AND FRAMES ==================================================================
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Day:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": animation_speed, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # ==== MAKE FRAMES ========================================================================
    frames_list = list()
    for day in df.index:
        frame = go.Frame(data=[], name=str(day))
        data_list = []
        for label in labels:
            dataset_by_day_label = df.loc[min(df.index):day, label]
            data_dict = {
                "x": list(dataset_by_day_label.index),  # list(day),
                "y": list(dataset_by_day_label.values),
                "mode": "lines+markers",
                "text": list(label),
                #                 "marker": {
                #                     "sizemode": "area",
                # #                     "sizeref": 200000,
                #                     "size": list(dataset_by_day_label.values)
                #                 },
                #                 "name": label
            }
            data_list.append(data_dict)
            frame["data"] = data_list
        frames_list.append(frame)

        slider_step = {"args": [
            [day],
            {"frame": {"duration": animation_speed, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": animation_speed}}
        ],
            "label": day,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    fig["frames"] = frames_list

    #     fig_dict["layout"]["sliders"] = [sliders_dict]
    # ===== END SLIDER AND FRAMES =====

    # ===== UPDATE LAYOUT, Axis, Margins, Size, Legend, Background =========================
    fig.update_layout(
        updatemenus=updatemenus,
        sliders=[sliders_dict],
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor=gray_color,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='#2cfec1', #'rgb(82, 82, 82)',
            ),
            #                 range=[0,max_x_range],
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(color='#2cfec1'),
            range=[0, max_y_range],
        ),
        autosize=False,
        margin=dict(
            autoexpand=True,
            # l=150,
            # r=0,
            # t=110,
            # b=90,
        ),
        showlegend=showlegend,
        legend_orientation="v",
        legend=dict(
            x=1.05,
            y=0, ),
        paper_bgcolor="#1f2630",  # "#F4F4F8",
        plot_bgcolor="#1f2630",  # 'white'
        font=dict(color='#2cfec1'),
        width=1200,
        height=600,
    )

    # ANNOTATIONS
    annotations = []
    # Adding labels
    for i, col in enumerate(df.columns):
        if col == doubling_column:
            # labeling x7 line
            y = 52  # df.loc[int(max(df.index/2)), 'x7']
            x = 40  # int(max(df.index)/2)
            annotations.append(dict(xref='x', x=x, y=y,
                                    xanchor='center', yanchor='middle',
                                    text="double every 7 days",
                                    font=dict(family='Arial',
                                              size=12,
                                              color=gray_color, ),
                                    showarrow=False))
            continue

        # labeling the left_side of the plot
        #     y = df.loc[min(df[col].dropna().index),col]
        #     annotations.append(dict(xref='paper', x=0.07, y=y,
        #                                   xanchor='right', yanchor='middle',
        #                                   text=col + ' {}'.format(y),
        #                                   font=dict(family='Arial',
        #                                             size=10),
        #                                   showarrow=False))

        # labeling the right_side of the plot
        x = max(df[col].dropna().index)
        y = df.loc[max(df[col].dropna().index), col]
        annotations.append(dict(xref='paper',
                                x=0.95,
                                y=y,
                                xanchor='left', yanchor='middle',
                                text=f"{col}: {int(y)}",
                                font=dict(family='Arial',
                                          size=12),
                                showarrow=False))

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0, y=1,
                            xanchor='left', yanchor='bottom',
                            text=title,
                            font=dict(family='Garamond',
                                      size=30,
                                      color='#7fafdf' #'rgb(37,37,37)'
                                      ),
                            showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.08,
                            xanchor='center', yanchor='top',
                            text="<a href=”https://www.rki.de/”> Data Source: Robert Koch Institute</a><br><i>Charts: Sergey Chekanskiy</i>",
                            font=dict(family='Arial',
                                      size=12,
                                      color='#7fafdf'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    return fig

