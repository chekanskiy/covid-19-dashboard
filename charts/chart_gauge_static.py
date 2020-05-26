import plotly.graph_objects as go
from datetime import timedelta
from plotly.subplots import make_subplots


def add_gauge(fig, region, max_value, current_value, yd_value, position):
    range_1 = max_value / 4
    range_2 = max_value / 1.7

    fig.add_trace(go.Indicator(
        mode="number+gauge+delta",
        gauge={'axis': {'range': [0, max_value * 1.1], 'tickwidth': 1, 'tickcolor': "darkblue"},
               # 'shape': "bullet",
               'bar': {'color': "#1f2630"},
               'bgcolor': "white",
               'borderwidth': 2,
               'bordercolor': "gray",
               'steps': [
                   {'range': [0, range_1], 'color': "#2AF598"},
                   {'range': [range_1, range_2], 'color': "#FFF57B"},
                   {'range': [range_2, max_value * 1.1], 'color': "#EF7F80"}],
               'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': max_value}},
        delta={'reference': yd_value},
        value=current_value,
        #         domain = {'x': [0, 1], 'y': [0.2, 0.9]},
        title={'text': f"{region}", 'font': dict(size=14)}),
        row=position[0], col=position[1]
    )
    return fig


def plot_gauges(df, column):
    # regions = len(df.region_wb.unique())

    plots = [{"type": 'indicator'} for i in range(8)]
    fig = make_subplots(rows=4, cols=2,
                        specs=[plots[0:2], plots[2:4], plots[4:6], plots[6:]],
                        vertical_spacing=0.15,
                        horizontal_spacing=0.1,
                        #                         column_widths=[0.3, 0.7],
                        #                         row_heights=[0.5, 0.5],
                        )
    print(fig.print_grid())
    reg_df_sum_total = df.groupby('region_wb').agg(['sum'])[column].sort_values(by='sum',
                                                                                         ascending=False).round(0)

    reg_df_max = df.reset_index(drop=True).groupby(['date', 'region_wb']).agg(['max'])[column].groupby(
        'region_wb').max()
    current_reg_df_sum = df.loc[df.index == df.index.max(), :].groupby('region_wb').agg(['sum'])[column].round(0)
    yd_reg_df_sum = df.loc[df.index == df.index.max() - timedelta(days=1), :].groupby('region_wb').agg(['sum'])[
        column].round(0)

    for i, region in enumerate(reg_df_sum_total.index.unique()):

        max_value = reg_df_max.reset_index().loc[reg_df_max.index == region, 'max'].values[0]
        current_value = current_reg_df_sum.reset_index().loc[current_reg_df_sum.index == region, 'sum'].values[0]
        yd_value = yd_reg_df_sum.reset_index().loc[yd_reg_df_sum.index == region, 'sum'].values[0]

        if i+1 <= 2:
            position = [1, i + 1]
        elif i+1 <= 4:
            position = [2, i + 1 - 2]
        elif i+1 <= 6:
            position = [3, i + 1 - 4]
        else:
            position = [4, i + 1 - 6]
        print(position)
        fig = add_gauge(fig, region, max_value, current_value, yd_value, position)

    fig.update_layout(paper_bgcolor='#1f2630',
                      font={'color': "rgb(204, 204, 204)", 'family': "Garamond"},
                      margin=dict(
                          autoexpand=True,
                          l=0,
                          r=0,
                          t=50,
                          b=10,
                      ),
                      )

    return fig
