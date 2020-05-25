import plotly.graph_objects as go
from plotly import colors


# def plot_map_express(df, geojson, column):
#     import plotly.express as px
#     fig = px.choropleth_mapbox(df, geojson=geojson, locations='iso_code', color=column,
#                                color_continuous_scale="YlGnBu",
#                                # range_color=(0, 200000000),
#                                # mapbox_style="mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz",
#                                mapbox_style="white-bg", #"carto-darkmatter",
#                                zoom=4, center = {"lat": 51.2, "lon": 10},
#                                opacity=1,
#                                labels={column:column},
#                                # width=600,
#                                # height=300
#                               )
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
#                       # plot_bgcolor = '#1f2630',
#                       # paper_bgcolor = '#1f2630'
#                      )
#     fig.update_traces(marker=dict(
#                       # size=1,
#                       line=dict(width=1,
#                                 color='#7fafdf')),
#                       # selector=dict(mode='markers')
#                       )
#     return fig


def plot_map_go(df, column, geojson=None, _colors=colors.diverging.Temps * 3,
                projection='mercator', fitbounds='locations'):
    color = '#1f2630'

    average_score = df[column].median()
    min_score = df[column].quantile(.1)
    max_score = df[column].quantile(.9)

    fig = go.Figure(data=go.Choropleth(
        locations=df['iso_code'],
        geojson=geojson,
        z=df[column],
        text=df['land'],
        colorscale= _colors, #'YlGnBu',
        reversescale=True,
        # autocolorscale=True,
        # zmax=20,
        # zmin=0,
        marker_line_color='#7fafdf',
        marker_line_width=0.5,
        zmid=average_score,
        zmax=max_score,
        zmin=min_score,
        # colorbar_tickprefix = '$',
        # colorbar_title='Confirmed Cases',
        showscale=False,
    ))
    fig.update_layout(
        # title_text='Confirmed Cases',
        dragmode="lasso",
        clickmode='event+select',
        geo=dict(
            showframe=False,
            projection=dict(type=projection),
            # projection_type="mercator", #go.layout.geo.Projection(type = 'Natural earth'), #'equirectangular'
            lataxis_range=[-55, 85],
            # lonaxis_range=[0, 200],
            # center=dict(lon=-30, lat=-30),
            # projection_rotation=dict(lon=30, lat=30, roll=0),
        ),
        plot_bgcolor=color,
        paper_bgcolor=color,
        autosize=True,
        # height=300,
        # width=1200,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[
            dict(
                x=0.55,
                y=0,
                xref='paper',
                yref='paper',
                text="Data Sources: <a href='https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Gesamt.html'>RKI</a>"
                     ", <a href='https://github.com/CSSEGISandData/COVID-19'>CSSE JHU</a>"
                     ", <a href='https://www.apple.com/covid19/mobility'>Apple</a><br>"
                     "<i>Dashboard: <a href='https://www.linkedin.com/in/sergeychekanskiy'>Sergey Chekanskiy</a></i>",
                font=dict(family='Garamond',
                          size=12,
                          color='#7fafdf'),
                showarrow=False,

            ),
            dict(
                x=0.05,
                y=0.96,
                xref='paper',
                yref='paper',
                text=f"Date: {str(df.index.max().date())}",
                font=dict(family='Garamond',
                          size=16,
                          color='#7fafdf',
                          ),
                showarrow=False,

            ),
        ]
    )


    fig.update_geos(
        fitbounds=fitbounds,
        visible=False,
        # resolution=50,
        showcoastlines=True,
        coastlinecolor=color,
        showland=True,
        landcolor=color,
        showocean=True,
        oceancolor=color,
        # showlakes=False,
        # lakecolor=color,
        showcountries=False,
        countrycolor=color,
        # showrivers=True,
        # rivercolor="Blue"
    )

    return fig
