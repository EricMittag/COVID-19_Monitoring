import pandas as pd
import numpy as np

import dash
dash.__version__
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import os
print(os.getcwd())
df=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')

countries = df['country'].unique()

fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Enterise Data Science TUK

    COVID-19 Dashboard

    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in countries],
        value=['United States', 'Germany', 'South Korea'], # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select Timeline of confirmed COVID-19 cases or the approximated doubling time
        '''),


    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
        {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
        {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
        {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
    ],
    value='confirmed',
    multi=False
    ),

    dcc.Graph(figure=fig, id='main_window_slope'),

    dcc.Markdown('''
    ## Select Y-Axis Scale
    '''),

    dcc.Dropdown(
        id='y_Axis_scale',
        options=[
            {'label': 'Linear', 'value': 'linear'},
            {'label': 'Logarithmic', 'value': 'log'}
        ],
        value='log',
        multi=False
    )
])



@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value'), 
    Input('y_Axis_scale', 'value')])
def update_figure(country_list,show_doubling, yAxis):


    if show_doubling == 'confirmed' or show_doubling == 'confirmed_filtered':
        my_yaxis={'type':yAxis,
               'title': 'Confirmed Infected People'
              }
    else:
        my_yaxis={'type':yAxis,
                  'title':'Doubling Rate in Days'
              }


    traces = []
    for each in country_list:

        df_plot=df[df['country']==each]

        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis=my_yaxis
        )
    }

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)
