import plotly.graph_objects as go
from plotly import colors

#  aliceblue, antiquewhite, aqua, aquamarine, azure,
#             beige, bisque, black, blanchedalmond, blue,
#             blueviolet, brown, burlywood, cadetblue,
#             chartreuse, chocolate, coral, cornflowerblue,
#             cornsilk, crimson, cyan, darkblue, darkcyan,
#             darkgoldenrod, darkgray, darkgrey, darkgreen,
#             darkkhaki, darkmagenta, darkolivegreen, darkorange,
#             darkorchid, darkred, darksalmon, darkseagreen,
#             darkslateblue, darkslategray, darkslategrey,
#             darkturquoise, darkviolet, deeppink, deepskyblue,
#             dimgray, dimgrey, dodgerblue, firebrick,
#             floralwhite, forestgreen, fuchsia, gainsboro,
#             ghostwhite, gold, goldenrod, gray, grey, green,
#             greenyellow, honeydew, hotpink, indianred, indigo,
#             ivory, khaki, lavender, lavenderblush, lawngreen,
#             lemonchiffon, lightblue, lightcoral, lightcyan,
#             lightgoldenrodyellow, lightgray, lightgrey,
#             lightgreen, lightpink, lightsalmon, lightseagreen,
#             lightskyblue, lightslategray, lightslategrey,
#             lightsteelblue, lightyellow, lime, limegreen,
#             linen, magenta, maroon, mediumaquamarine,
#             mediumblue, mediumorchid, mediumpurple,
#             mediumseagreen, mediumslateblue, mediumspringgreen,
#             mediumturquoise, mediumvioletred, midnightblue,
#             mintcream, mistyrose, moccasin, navajowhite, navy,
#             oldlace, olive, olivedrab, orange, orangered,
#             orchid, palegoldenrod, palegreen, paleturquoise,
#             palevioletred, papayawhip, peachpuff, peru, pink,
#             plum, powderblue, purple, red, rosybrown,
#             royalblue, rebeccapurple, saddlebrown, salmon,
#             sandybrown, seagreen, seashell, sienna, silver,
#             skyblue, slateblue, slategray, slategrey, snow,
#             springgreen, steelblue, tan, teal, thistle, tomato,
#             turquoise, violet, wheat, white, whitesmoke,
#             yellow, yellowgreen


def plot_bar_static(df, selected_column, categories_column='region_wb', _colors=colors.diverging.Temps * 3):
    bg_color = '#1f2630'
    text_color = '#2cfec1'
    gray_color = 'rgb(204, 204, 204)'
    fig = go.Figure()
    categories_sorted = df.groupby(by=categories_column)[selected_column].sum().sort_values(ascending=False).index
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