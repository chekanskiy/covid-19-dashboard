# Fully interactive dashboard for Germany and the World
Disclamer: this is a personal project to explore dynamic dashboarding with Plotly Dash and to stay on top of the developments of the pandemic in the world.

## Deployed version: https://dashboard-covid-19-dash.herokuapp.com/

Switch between the world view and the dashboard for Germany.
Select countries the map by clicking/dragging or search in the drop-down menu.
Choose a specific date by clicking on the corresponding point on the top left chart.

![Main view](images/dashboard.png)

![Boxplot view](images/dashboard2.png)

## Repository structure
app.py - the main application, layout definition and callbacks for the interactivity
assets/ - css files containing 90% of the visual layout 
charts/ - contains functions to draw charts
data/ - data files that power the dashboard

Data Sources:
* <a href='https://www.rki.de/'>Robert Koch Institute</a><br>
* <a href='https://github.com/CSSEGISandData/COVID-19'>CSSE JHU</a>
* <a href='https://data.worldbank.org/'>World Bank</a>
* <a href='https://www.apple.com/covid19/mobility'>Apple Mobility</a><br>
* <a href='https://www.naturalearthdata.com/'>Natural Earth</a><br>
