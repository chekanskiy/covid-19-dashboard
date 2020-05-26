import plotly.graph_objects as go
from plotly import colors


def plot_bar_static(df, selected_column, categories_column='region_wb', _colors=colors.diverging.Temps * 3):
    bg_color = '#1f2630'
    text_color = '#2cfec1'
    gray_color = 'rgb(204, 204, 204)'
    fig = go.Figure()
    categories_sorted = df.groupby(by=categories_column)[selected_column].sum().sort_values(ascending=False).index
    # _min_y_range = df.loc[:, selected_column].quantile(0.01)
    # _max_y_range = df.loc[:, selected_column].quantile(0.98)

    for i, region in enumerate(categories_sorted):
        fig.add_trace(go.Bar(
            x=df.loc[df[categories_column] == region, 'land'],
            y=df.loc[df[categories_column] == region, selected_column],
            name=region,
            marker=dict(color=_colors[i],  # 'lightskyblue',
                        opacity=0.7,
                        line=dict(
                            color=gray_color,
                            width=1
                        )
                        )))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-90,
                      plot_bgcolor=bg_color,
                      paper_bgcolor=bg_color,
                      yaxis=dict(
                          showline=True,
                          showgrid=False,
                          #         title='',
                          #         titlefont_size=16,
                          #         tickfont_size=14,
                          # range=[_min_y_range, _max_y_range],
                          tickfont_color=text_color
                      ),
                      xaxis=dict(
                          #         title='',
                          #         titlefont_size=16,
                          #         tickfont_size=14,
                          tickfont_color=text_color
                      ),
                      legend_orientation="h",
                      legend=dict(
                          x=0,
                          y=1.3,),
                      margin=dict(
                          autoexpand=True,
                          l=10,
                          r=10,
                          t=50,
                          b=10,
                      ),
                      )
    return fig