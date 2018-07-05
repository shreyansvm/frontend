import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from pandas_datareader import data as web
import pandas_datareader as pdr
import datetime

app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Nvidia', 'value': 'NVDA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Twitter', 'value': 'TWTR'},
            {'label': 'Facebook', 'value': 'FB'},
            {'label': 'Shopify', 'value': 'SHOP'}
        ],
        value='COKE'
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
    app.run_server()