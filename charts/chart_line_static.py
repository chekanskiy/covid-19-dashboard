from numpy import log10, datetime64, dtype
import pandas as pd
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from plotly import colors


def plot_lines_plotly(df, column, _colors=colors.diverging.Temps * 3,
                      title=False, show_doubling=True, doubling_days=7, showlegend=False):

    _doubling_column = f'double_x{doubling_days}'

    if show_doubling:
        def double_every_x_days(day, days_doubling, start_value=1):
            r = start_value * 2 ** (day / days_doubling)
            return r

        start_value = df.loc[(df[column] > 0) & (df.index == df.index.min()), column].median()
        if start_value < 1:
            start_value = 1

        # prepare empty dataframe to fill in
        date_range = pd.date_range(df.index.min(), df.index.max())
        df_index = pd.DataFrame(columns=['date', 'land', column],
                                data={'date': date_range, 'land': _doubling_column},
                                )
        # create a column with rank 1,2,3 etc for every 'land' in this case doubling types
        df_index['rn'] = df_index.groupby('land')['date'].rank(method='first', ascending=True)
        df_index[column] = df_index['rn'].apply(lambda x: double_every_x_days(x, doubling_days, start_value))
        df_index['date'] = df_index['date'].astype('datetime64[ns]')
        df_index.set_index('date', inplace=True, drop=False)
        df_index.sort_index(inplace=True, ascending=True)
        del df_index['rn']
        df = df.append(df_index, ignore_index=False, verify_integrity=False, sort=True)
        # df = df.rename_axis('dates_index').sort_values(by=['land', 'dates_index'], ascending=[True, True])

    # Create traces
    fig = go.Figure()

    _labels = df['land'].unique()

    #     max_x_range = len(df.index)
    _max_y_range = df.loc[df.land != _doubling_column, column].max() * 1.1
    if df.loc[:, column].min() > 0:
        _min_y_range = df.loc[(df.land != _doubling_column) & (df[column] > 0), column].min() / 2
    else:
        _min_y_range = df.loc[(df.land != _doubling_column), column].min() * 1.1

    _symbols = [x for i, x in enumerate(SymbolValidator().values) if i % 2 != 0]  # all markers
    _gray_color = 'rgb(204, 204, 204)'

    _mode_size = [8] * len(_labels)  # [8, 8, 12, 8]
    _line_size = [1] * len(_labels)  # [2, 2, 4, 2]

    for i, l in enumerate(_labels):
        # Adding Doubling x7 line
        if l == _doubling_column:
            fig.add_trace(go.Scatter(x=df.loc[df.land == l].index,
                                     y=df.loc[df.land == l, column],
                                     mode='lines',
                                     marker=dict(color=_gray_color,
                                                 size=_mode_size[i] - 2,
                                                 opacity=0.7,
                                                 symbol=_symbols[i + 2],
                                                 line=dict(
                                                     color=_colors[i],
                                                     width=1
                                                 )
                                                 ),
                                     name=l,
                                     line=dict(color=_gray_color,
                                               width=_line_size[i],
                                               dash='dot', ),
                                     connectgaps=True,
                                     ))
        # Adding all other lines
        else:
            fig.add_trace(go.Scatter(x=df.loc[df.land == l].index,
                                     y=df.loc[df.land == l, column],
                                     mode='lines+markers',
                                     marker=dict(color=_colors[i],
                                                 size=_mode_size[i] - 1,
                                                 opacity=0.7,
                                                 symbol=_symbols[i + 2],
                                                 line=dict(
                                                     color=_colors[i],
                                                     width=1
                                                 )
                                                 ),
                                     name=l,
                                     line=dict(color=_colors[i],
                                               width=_line_size[i]),
                                     connectgaps=False,
                                     ))

            # endpoints
            min_index, max_index = df.loc[df.land == l].index.min(), df.loc[df.land == l].index.max()
            fig.add_trace(go.Scatter(
                x=[min_index, max_index],
                y=[df.loc[(df.index == min_index) & (df.land == l)], df.loc[(df.index == max_index) & (df.land == l)]],
                mode='markers',
                name=l,
                marker=dict(color=_colors[i], size=_mode_size[i] + 2, ),
                showlegend=False,
            ))
        if 'confirmed_peak_date' in df.columns:
            # Mark when the peak is reached
            peak_index = df.loc[(df.land == l) & (df['confirmed_peak_date'] == 1), column].index.tolist()
            fig.add_trace(go.Scatter(
                x=peak_index,
                y=df.loc[(df.index.isin(peak_index)) & (df.land == l), column].tolist(),
                # y=[df.loc[(df.index == peak_index) & (df.land == l), column]],
                mode='markers',
                name=f"Peak {l}",
                marker=dict(
                    color='#008000',
                    size=15,
                    opacity=1,
                    symbol='triangle-down',
                    line=dict(
                        # color=_colors[i],
                        width=1
                    )),
                showlegend=False,
            ))
            # Mark when the new peak is starting (new wave is approaching)
            peak_index = df.loc[(df.land == l) & (df['confirmed_peak_date'] == -1), column].index.tolist()
            fig.add_trace(go.Scatter(
                x=peak_index,
                y=df.loc[(df.index.isin(peak_index)) & (df.land == l), column].tolist(),
                mode='markers',
                name=f"New Wave {l}",
                marker=dict(
                    color='#FF0000',
                    size=15,
                    opacity=1,
                    symbol='triangle-up',
                    line=dict(
                        # color=_colors[i],
                        width=1
                    )),
                showlegend=False,
            ))
            # # Mark when we predict the perk to be reached
            # peak_index = df.loc[(df.land == l) & (df['peak_log_trend'] < 0), column].index.tolist()
            # fig.add_trace(go.Scatter(
            #     x=peak_index,
            #     # y=[df.loc[df['peak_log_trend'] < 0, column].max().round(2)],
            #     y=df.loc[(df.index.isin(peak_index)) & (df.land == l), column].tolist(),
            #     mode='lines+markers',
            #     name=f"fc: {l}",
            #     marker=dict(
            #         color=_colors[i],
            #         size=20,
            #         opacity=1,
            #         symbol='triangle-up',
            #         line=dict(
            #             color=_colors[i],
            #             width=1
            #         )),
            #     showlegend=False,
            # ))

    # BUTTONS Changing Y Scale
    updatemenus = list([
        dict(active=1,
             direction="left",
             buttons=list([
                 dict(label='Log',
                      method='update',
                      args=[{'visible': [True, True]},
                            {  # 'title': 'Log scale',
                                'yaxis': {'type': 'log', 'range': [log10(_min_y_range), log10(_max_y_range)],
                                          'showgrid': False,
                                          'zeroline': False,
                                          'showline': False,
                                          'linecolor': '#1f2630',
                                          }}
                            ]
                      ),
                 dict(label='Linear',
                      method='update',
                      args=[{'visible': [True, True]},
                            {  # 'title': 'Linear scale',
                                'yaxis': {'type': 'linear', 'range': [_min_y_range, _max_y_range],
                                          # 'showticklabels': False,
                                          'showgrid': False,
                                          'zeroline': False,
                                          'showline': False,
                                          'linecolor': '#1f2630',
                                          }}
                            ]
                      ),
             ]),
             type='buttons',
             pad={"r": 10, "t": 10},
             showactive=True,
             x=0.10,
             xanchor="left",  # ['auto', 'left', 'center', 'right']
             y=1,
             yanchor='top',  # ['auto', 'top', 'middle', 'bottom']
             )
    ])

    # UPDATE LAYOUT, Axis, Margins, Size, Legend, Background
    fig.update_layout(
        updatemenus=updatemenus,
        dragmode="select",
        clickmode='event+select',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor=_gray_color,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='#2cfec1',  # 'rgb(82, 82, 82)',
            ),
            #                 range=[0,max_x_range],
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(color='#2cfec1'),
            range=[_min_y_range, _max_y_range],
        ),
        margin=dict(
            autoexpand=True,
            l=10,
            r=100,
            t=10,
            b=100,
        ),
        showlegend=showlegend,
        legend_orientation="v",
        legend=dict(
            x=1.05,
            y=0, ),
        paper_bgcolor="#1f2630",  # "#F4F4F8",
        plot_bgcolor="#1f2630",  # 'white'
        font=dict(color='#2cfec1'),
        autosize=True,
        # width=800,
        # height=500,
    )

    # ANNOTATIONS
    annotations = []
    # Adding labels
    for i, l in enumerate(_labels):
        min_index, max_index = df.loc[df.land == l].index.min(), df.loc[df.land == l].index.max()
        if l == _doubling_column:
            # labeling x7 line
            x = (min_index + (max_index - min_index) / 2)
            try:
                x = str(x.date())
            except:
                pass
            y = df.loc[(df.land == l) & (df.index == x), column].values[0]
            annotations.append(dict(xref='x', x=x, y=y,
                                    xanchor='center', yanchor='middle',
                                    text="double every 7 days",
                                    font=dict(family='Arial',
                                              size=12,
                                              color=_gray_color, ),
                                    showarrow=False))
        else:
            # labeling the right_side of the plot
            y = df.loc[(df.land == l) & (df.index == max_index), column].values[0]
            annotations.append(dict(xref='paper',
                                    x=0.95,
                                    y=y,
                                    xanchor='left', yanchor='middle',
                                    text=l,  # f"{col}: {int(y)}",
                                    font=dict(family='Arial',
                                              size=12,
                                              color=_colors[i]),
                                    showarrow=False))

            # ======================================= ANNOTATE DATA OUTLIERS ========================
            annotation_style_outliers = dict(
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.2,
                arrowwidth=1.2,
                arrowcolor=_gray_color,
                # bordercolor=_gray_color,
                # borderwidth=2,
                # borderpad=4,
                # bgcolor=_gray_color,  # "#ff7f0e"
                opacity=0.5,
                ax=0,
                ay=-40,
                font=dict(family='Garamond',
                          size=12,
                          color=_gray_color
                          ),
            )
            if l == 'Hamburg':
                try:
                    annotation = annotation_style_outliers
                    annotation['text'] = 'HH: Recorded old cases'
                    x = df.loc[(df.date == '2020-05-12') & (df.land == l), [column]].index[0]
                    y = df.loc[(df.index == x) & (df.land == l), column].values[0]
                    annotation['x'] = x
                    annotation['y'] = df.loc[(df.index == x) & (df.land == l), column].values[0]
                    annotations.append(annotation)
                except:
                    pass
            # =================================== END ANNOTATE DATA OUTLIERS ========================

    # Title
    if title:
        annotations.append(dict(xref='paper', yref='paper', x=0, y=1,
                                xanchor='left', yanchor='bottom',
                                text=title,
                                font=dict(family='Garamond',
                                          size=30,
                                          color='#7fafdf' #'rgb(37,37,37)'
                                          ),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.06,
                            xanchor='center', yanchor='top',
                            text="Data Source: <a href='https://www.rki.de/'>Robert Koch Institute</a>"
                                 ", <a href='https://www.apple.com/covid19/mobility'>Apple</a><br>"
                                 "<i>Charts: <a href='https://www.linkedin.com/in/sergeychekanskiy'>Sergey Chekanskiy</a></i>",
                            font=dict(family='Garamond',
                                      size=12,
                                      color='#7fafdf'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    return fig
