import plotly.graph_objects as go
import pandas as pd
from plotly import colors


def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    levels = [level for level in levels if level is not None]

    if color_columns is not None:
        cols = ['id', 'parent', 'value', 'color']
        df.loc[df[color_columns[0]] < 0, color_columns[0]] = 0
        df.loc[df[color_columns[1]] < 0, color_columns[1]] = 0
        df.loc[df[value_column] < 0, value_column] = 0
    else:
        cols = ['id', 'parent', 'value']
        df.loc[df[value_column] < 0, value_column] = 0

    df_all_trees = pd.DataFrame(columns=cols)
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=cols)
        # Aggregating by all levels to the right of current
        dfg = df.groupby(levels[i:]).sum()  # Aggregation Fanction
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()  # Fill in ID column
        if i < len(levels) - 1:  # Setting PARENT value, the next column untill the last one, after which it is TOTAL
            df_tree['parent'] = dfg[levels[i + 1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        if color_columns is not None:
            df_tree['color'] = dfg[color_columns[0]] * 1.0 / dfg[color_columns[1]]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    if color_columns is not None:
        total_dict = dict(id='total', parent='',
                          value=df[value_column].sum(),
                          color=df[color_columns[0]].sum() * 1.0 / df[color_columns[1]].sum())
    else:
        total_dict = dict(id='total', parent='',
                          value=df[value_column].sum(),)
    total = pd.Series(total_dict)
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees


def plot_sunburst_static(df, value_column,
                         levels=['land', 'region_wb'],
                         color_columns=None,
                         _colors=colors.sequential.PuBu,
                         value_column_name=''):
    color = '#1f2630'

    df_sunburst = build_hierarchical_dataframe(df, levels, value_column, color_columns)

    if color_columns is not None:
        hovertemplate = '<b>%{label} </b> <br> ' + value_column_name + ': %{value}<br>     per 100k: %{color:.0f}'
        average_score = df_sunburst['color'].median()
        min_score = df_sunburst['color'].quantile(.1)
        max_score = df_sunburst['color'].quantile(.9)
        fraction_series = df_sunburst['color']
    else:
        hovertemplate = '<b>%{label} </b> <br> ' + value_column_name + ': %{value}<br>'
        average_score = df[value_column].median()
        min_score = df[value_column].quantile(.1)
        max_score = df[value_column].quantile(.9)
        fraction_series = df[value_column]

    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        labels=df_sunburst['id'],
        parents=df_sunburst['parent'],
        values=df_sunburst['value'],
        branchvalues='total',
        marker=dict(
            colors=fraction_series,
            colorscale=_colors,
            # reversescale=True,
            cmid=average_score,
            cmax=max_score,
            cmin=min_score
        ),
        hovertemplate=hovertemplate,
        name=''
    ))

    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10),
                      plot_bgcolor=color,
                      paper_bgcolor=color,
                      )
    return fig