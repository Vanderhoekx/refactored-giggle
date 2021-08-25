from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import os


athletes_df = pd.read_excel(os.path.join('datasets', 'olympics2021', 'Athletes.xlsx'), engine='openpyxl')
medals_df = pd.read_excel(os.path.join('datasets', 'olympics2021', 'Medals.xlsx'), engine='openpyxl')

athletes_group = athletes_df.groupby(['NOC', 'Discipline']).count().reset_index()
sports_group = athletes_df.groupby('Discipline').count().reset_index()
medals_group = medals_df.groupby(['Team/NOC', 'Gold', 'Silver', 'Bronze', 'Total']).count().reset_index()

medals_average = {}
for country, total in zip(medals_group['Team/NOC'], medals_group['Total']):
    medals_average.setdefault(country, total // sum(medals_group['Total']))

print(medals_average)
average_medals_won = sum(medals_group['Total']) // len(medals_group['Team/NOC'])
average_athletes_sport = sum(sports_group['Name']) // len(sports_group['Discipline'])


fig = make_subplots(
    rows = 8,
    cols = 2,
    specs = [[{'type': 'bar', 'colspan': 2, 'rowspan': 2}, None],
            [{'type': 'scatter', 'colspan': 2}, None],
            [None, None],
            [None, None],
            [{'type': 'scatter', 'colspan': 2, 'rowspan': 2}, None],
            [{'type': 'scatter', 'colspan': 2}, None],
            [None, None],
            [None, None],])

fig.add_trace(
    go.Bar(x = athletes_group['Discipline'],
        y = athletes_group['Name'],
        name = 'Country',
        marker = {
        'color': 'orange'
        },
        hovertext = athletes_group['NOC'],
        marker_line_width = 0.25,),
        row = 1, col = 1)

fig.add_trace(
    go.Scatter(x = athletes_group['Discipline'],
        y = [average_athletes_sport] * len(athletes_group['Discipline']),
        name = 'Average Athlete by Sport',
        mode = 'lines',
        marker = {
            'color': 'green'
        },
        opacity = 0.25,
        hovertext = 'Average Athletes/Sport'),
        row = 1, col = 1
)

fig.add_trace(
    go.Scatter(x = medals_group['Team/NOC'],
        y = medals_group['Total'],
        name = 'Medals',
        mode = 'markers',
        marker = {
        'color': 'red',
        },
        hovertext = medals_group['Total'],),
        row = 5, col = 1)   

fig.add_trace(
    go.Scatter(x = medals_group['Team/NOC'],
        y = [average_medals_won] * len(medals_group['Team/NOC']),
        mode = 'lines',
        name = 'Average Medals Won',
        marker = {
            'color': 'blue',
    },
    opacity = 0.25,
    hovertext = 'Average Medals Won'),
    row = 5, col = 1
    )

fig.update_yaxes(title_text = 'No. of Athletes', row = 1, col = 1)
fig.update_yaxes(title_text = 'Total Medals', row = 5, col = 1)

fig.show()
