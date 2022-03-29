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

axon_name='D:\Complete_points\AL110axons_region_with_counts.xls'
df_axon=pd.read_excel(axon_name.lstrip('\u202a'))

dendrite_name='D:\Complete_points\AL110dendrites_region_with_counts.xls'
df_dendrite=pd.read_excel(dendrite_name.lstrip('\u202a'))

def plot_bar(df_axon,df_dendrite):
    fig = make_subplots(
        rows=2, cols=2,
        shared_yaxes=True,
        row_heights=[0.9, 0.1],
        column_titles=['Length (um)','# of endings'], 
        row_titles=['Axons', 'Dendrites'],
    )

    fig.add_trace(go.Bar(y=df_axon['acronym'], x=df_axon['Total_counts'],
                  marker_color='olive',
                  name='',
                  text=df_axon['name'],
                  hovertemplate=
                  '<i>%{x}</i>, '+
                  '<b>%{text}</b>',
                  orientation='h'),
                  row=1, col=1)

    fig.add_trace(go.Bar(y=df_axon['acronym'], x=df_axon['Endings_counts'],
                  marker_color='seagreen',
                  name='',
                  text=df_axon['name'],
                  hovertemplate=
                  '<i>%{x}</i>, '+
                  '<b>%{text}</b>',
                  orientation='h'),
                  row=1, col=2)

    fig.add_trace(go.Bar(y=df_dendrite['acronym'], x=df_dendrite['Total_counts'],
                  marker_color='blue',
                  name='',
                  text=df_dendrite['name'],
                  hovertemplate=
                  '<i>%{x}</i>, '+
                  '<b>%{text}</b>',
                  orientation='h'),
                  row=2, col=1)

    fig.add_trace(go.Bar(y=df_dendrite['acronym'], x=df_dendrite['Endings_counts'],
                  marker_color='lightblue',
                  name='',
                  text=df_dendrite['name'],
                  hovertemplate=
                  '<i>%{x}</i>, '+
                  '<b>%{text}</b>',
                  orientation='h'),
                  row=2, col=2)

    fig.update_layout(height=700, showlegend=False,yaxis={'categoryorder':'total ascending'})
    return fig

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
    
    dcc.Graph(id='graph')
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
    Output('graph', 'figure'),
    [Input('brains-radio', 'value')])
def update_graph(selected_brains):
    brain='\\' + selected_brains
    axon_name='D:\Complete_points'+ brain + 'axons_region_with_counts.xls'
    df_axon=pd.read_excel(axon_name.lstrip('\u202a'))

    dendrite_name='D:\Complete_points'+ brain + 'dendrites_region_with_counts.xls'
    df_dendrite=pd.read_excel(dendrite_name.lstrip('\u202a'))

    return plot_bar(df_axon,df_dendrite)


if __name__ == '__main__':
    app.run_server(debug=True)