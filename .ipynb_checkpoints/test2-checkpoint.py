import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "bar"}, {"type": "barpolar"}],
           [{"type": "pie"}, {"type": "scatter3d"}]],
)

fig.add_trace(go.Bar(y=[2, 3, 1]),
              row=1, col=1)

fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),
              row=1, col=2)

fig.add_trace(go.Pie(values=[2, 3, 1]),
              row=2, col=1)

fig.add_trace(go.Scatter3d(x=[2, 3, 1], y=[0, 0, 0], 
                           z=[0.5, 1, 2], mode="lines"),
              row=2, col=2)

fig.update_layout(height=700, showlegend=False)

all_options = {
    'GFP': ['AL110', 'AL126', 'AL131','Al140' ,'AL142'],
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
              figure=fig)
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
    brain='\\' + selected_brains
    name='D:\Complete_points' + brain + 'axons_region_with_counts.xls'
    df=pd.read_excel(name.lstrip('\u202a'))
    df=df.sort_values(by=['Total_counts'])
    return fig








if __name__ == '__main__':
    app.run_server(debug=True)