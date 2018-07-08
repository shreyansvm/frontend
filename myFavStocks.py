import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from pandas_datareader import data as web
import pandas_datareader as pdr
import datetime

app = dash.Dash()

app.layout = html.Div([
    html.H1('BytePython Ventures', className='banner'),
    html.Div([
        html.P('Welcome to BytePython Ventures - Investments'),
        html.P('Currently our investments range from Tech to Pharma to Energy.')
    ]),

    ### TODO : This functionality not yet working. Handle how user-selected start and end time can be passed to callback method
    html.Div([
        html.P("Start-Time"),
        dcc.Dropdown(id='start_time', options=[
                     {'label': i, 'value': i} for i in ['Jan 1st 2016', 'Jan 1st 2017', 'Jan 1st 2018']], value='Jan 1st 2018')
    ], style={'width': '40%', 'margin-left': '3%', 'display': 'inline-block'}),

    html.Div([
        html.P("End-Time"),
        dcc.Dropdown(id='end_time', options=[
                     {'label': i, 'value': i} for i in ['Jan 1st 2016', 'Jan 1st 2017', 'Jan 1st 2018']], value='Jan 1st 2018')
    ], style={'width': '31%', 'margin-left': '3%', 'display': 'inline-block'}),

    html.Div([
        html.P("Please select the stock from the drop-down to view its current stock price between the above start and end dates")
    ]),
    ######################

    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Nvidia', 'value': 'NVDA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'AbbVie', 'value': 'ABBV'},
            {'label': 'Facebook', 'value': 'FB'},
            {'label': 'Shopify', 'value': 'SHOP'},
            {'label': 'Twitter', 'value': 'TWTR'},
            {'label': 'JPMorgan Chase & Co', 'value': 'JPM'},
            {'label': 'Exxon Mobil Corp', 'value': 'XOM'},
        ],
        value='NVDA'
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    start = datetime.datetime(2018, 1, 1)
    end = datetime.date.today()
    df = pdr.get_data_yahoo(selected_dropdown_value, start, end)
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }]
    }

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8888)