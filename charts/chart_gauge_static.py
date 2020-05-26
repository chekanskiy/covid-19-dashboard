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


def plot_gauges(df, value_column, aggregate_by_column='region_wb'):
    # regions = len(df[aggregate_by_column].unique())

    LAYOUT_MAX_CHARTS = 8

    plots = [{"type": 'indicator'} for i in range(LAYOUT_MAX_CHARTS)]
    fig = make_subplots(rows=4, cols=2,
                        specs=[plots[0:2], plots[2:4], plots[4:6], plots[6:]],
                        vertical_spacing=0.15,
                        horizontal_spacing=0.1,
                        #                         column_widths=[0.3, 0.7],
                        #                         row_heights=[0.5, 0.5],
                        )

    if '_per_100k' in value_column:
        # Recalculate Values per Population per Region for accuracy
        # Get original column
        column_original = value_column.replace('_per_100k', '')
        # Sum population per region
        reg_df_sum_population = df.groupby(aggregate_by_column).agg(['sum'])['population_100k']
        reg_df_sum_population.columns = ['population']

        # Aggregate maximum value for the dates and regions
        reg_df_max = df.reset_index(drop=True).groupby(['date', aggregate_by_column]).agg(['sum'])[column_original].groupby(aggregate_by_column).agg(['max'])
        reg_df_max.columns = ['max']
        # Aggregate most recent day's value for regions
        current_reg_df_sum = df.loc[df.date == df.date.max(), :].groupby(aggregate_by_column).agg(['sum'])[column_original]
        # Aggregate yesterday's value for regions
        yd_reg_df_sum = df.loc[df.date == df.date.max() - timedelta(days=1), :].groupby(aggregate_by_column).agg(['sum'])[column_original]

        # Join population
        reg_df_max = reg_df_max.join(reg_df_sum_population)
        current_reg_df_sum = current_reg_df_sum.join(reg_df_sum_population)
        yd_reg_df_sum = yd_reg_df_sum.join(reg_df_sum_population)

        # Normalise values for population
        reg_df_max['max'] = reg_df_max['max'] / reg_df_max['population']
        current_reg_df_sum['sum'] = current_reg_df_sum['sum'] / current_reg_df_sum['population']
        yd_reg_df_sum['sum'] = yd_reg_df_sum['sum'] / yd_reg_df_sum['population']
    else:
        # Aggregate maximum value for the dates and regions
        reg_df_max = df.reset_index(drop=True).groupby(['date', aggregate_by_column]).agg(['max'])[value_column].groupby(aggregate_by_column).max()
        # Aggregate most recent day's value for regions
        current_reg_df_sum = df.loc[df.date == df.date.max(), :].groupby(aggregate_by_column).agg(['sum'])[value_column]
        # Aggregate yesterday's value for regions
        yd_reg_df_sum = df.loc[df.date == df.date.max() - timedelta(days=1), :].groupby(aggregate_by_column).agg(['sum'])[value_column]

    # Sort values to sort charts below
    current_reg_df_sum = current_reg_df_sum.sort_values(by='sum', ascending=False)

    aggregated_categories = current_reg_df_sum.index.unique()
    display_values = min([len(aggregated_categories), LAYOUT_MAX_CHARTS])

    for i, region in enumerate(aggregated_categories[:display_values]):

        max_value = reg_df_max.reset_index().loc[reg_df_max.index == region, 'max'].round(3).values[0]
        current_value = current_reg_df_sum.reset_index().loc[current_reg_df_sum.index == region, 'sum'].round(3).values[0]
        yd_value = yd_reg_df_sum.reset_index().loc[yd_reg_df_sum.index == region, 'sum'].round(3).values[0]

        if i+1 <= 2:
            position = [1, i + 1]
        elif i+1 <= 4:
            position = [2, i + 1 - 2]
        elif i+1 <= 6:
            position = [3, i + 1 - 4]
        else:
            position = [4, i + 1 - 6]
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
