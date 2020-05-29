import plotly.graph_objects as go
from datetime import timedelta
from plotly.subplots import make_subplots


def add_gauge(fig, region, current_value, yd_value, position):
    fig.add_trace(go.Indicator(
        mode="number+delta",
        delta={'reference': yd_value},
        value=current_value,
        #         domain = {'x': [0, 1], 'y': [0.2, 0.9]},
        title={'text': f"{region}",
               'font': dict(size=12)
               }),
        row=position[0], col=position[1]
    )
    return fig


def plot_numbers(df, value_column, aggregate_by_column='region_wb'):
    LAYOUT_MAX_CHARTS = 9

    plots = [{"type": 'indicator'} for i in range(LAYOUT_MAX_CHARTS)]
    fig = make_subplots(rows=1, cols=9,
                        specs=[plots[0:]],
                        # vertical_spacing=0.15,
                        # horizontal_spacing=0.1,
                        # column_widths=[2, 0.5, 0.5, 0.85, 0.5, 0.5, 0.5, 0.5, 0.5],
                        # row_heights=[0.1],
                        )

    # Aggregate most recent day's value for regions
    current_reg_df_sum = df.loc[df.date == df.date.max(), :].groupby(aggregate_by_column).agg(['sum'])[value_column]
    # Aggregate yesterday's value for regions
    yd_reg_df_sum = df.loc[df.date == df.date.max() - timedelta(days=1), :].groupby(aggregate_by_column).agg(['sum'])[
        value_column]

    # Sort values to sort charts below
    current_reg_df_sum = current_reg_df_sum.sort_values(by='sum', ascending=False)

    aggregated_categories = current_reg_df_sum.index.unique()
    display_values = min([len(aggregated_categories), LAYOUT_MAX_CHARTS])

    fig = add_gauge(fig, 'World', current_reg_df_sum.sum()['sum'], yd_reg_df_sum.sum()['sum'], [1, 1])

    for i, region in enumerate(aggregated_categories[:display_values]):
        current_value = current_reg_df_sum.reset_index().loc[current_reg_df_sum.index == region, 'sum'].round(3).values[
            0]
        yd_value = yd_reg_df_sum.reset_index().loc[yd_reg_df_sum.index == region, 'sum'].round(3).values[0]

        position = [1, i + 2]

        fig = add_gauge(fig, region, current_value, yd_value, position)

    fig.update_layout(paper_bgcolor='#1f2630',
                      font={'color': "rgb(204, 204, 204)", 'family': "Garamond"},
                      margin=dict(
                          autoexpand=True,
                          l=0,
                          r=0,
                          t=50,
                          b=10,
                      ),
                      height=120,
                      # width=1600
                      )

    return fig


# plot_numbers(df, 'confirmed', aggregate_by_column='region_wb')
