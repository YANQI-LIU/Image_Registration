import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

import plotly
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

name='D:\\AL110\\axons_RegionCounts.xlsx'
df=pd.read_excel(name.lstrip('\u202a'))

all_options = {
    'GFP': ['AL110', 'Al126', 'AL131'],
    'mGFP': ['AL080', 'GF243'],
    'Mixed plasmid': ['AL066', 'AL092'],
}
app.layout = html.Div([
    dcc.RadioItems(
        id='plasmids-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='GFP'
    ),

    html.Hr(),

    dcc.RadioItems(id='brains-radio'),

    html.Hr(),

    html.Div(id='display-selected-values'),
    
    dcc.Graph(id='graph',
              figure={
                  'data':[{
                      'x':df['Total_counts'], 'y':df['acronym'], 'text':df['name'], 'type':'bar', 'orientation': 'h'
                  }]
              }
             )
])


@app.callback(
    Output('brains-radio', 'options'),
    [Input('plasmids-radio', 'value')])
def set_brains_options(selected_plasmids):
    return [{'label': i, 'value': i} for i in all_options[selected_plasmids]]


@app.callback(
    Output('brains-radio', 'value'),
    [Input('brains-radio', 'options')])
def set_brain_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('plasmids-radio', 'value'),
     Input('brains-radio', 'value')])
def set_display_children(selected_plasmids, selected_brains):
    return u'{} was electroporated with {}'.format(
        selected_brains,selected_plasmids
    )

@app.callback(
    Output('graph', 'figure'),
    [Input('brains-radio', 'value')])
def update_graph(selected_brains):
    name='D:\\' + selected_brains+'\\axons_RegionCounts.xlsx'
    df=pd.read_excel(name.lstrip('\u202a'))
    return {
        'data': [{'x':df['Total_counts'], 'y':df['acronym'], 'text':df['name'], 'type':'bar', 'orientation': 'h'
        }]
    }


if __name__ == '__main__':
    app.run_server(debug=True)