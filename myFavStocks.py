import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from pandas_datareader import data as web
import pandas_datareader as pdr
import datetime
import crunchbase as crunchbase
import newsapi as newsapi

app = dash.Dash()

app.layout = html.Div([
    html.H1('BytePython Ventures', className='banner'),
    html.Div([
        html.P('Welcome to BytePython Ventures - Investments'),
        html.P('Currently our investments range from Tech to Pharma to Energy.')
    ]),

    html.Div([
        html.P("Start-Time"),
        dcc.Dropdown(id='start_time',
            options=[
                {'label': 'Last 6 Months', 'value':'last_6_mnths'},
                {'label': 'Last 1 Year', 'value': 'last_1_yr'},
                {'label': 'Last 5 Years', 'value': 'last_5_yrs'}
            ],
            value='last_1_yr')
        ], style={'width': '40%', 'margin-left': '3%', 'display': 'inline-block'}),

    ### TODO : Get more options for end-date
    html.Div([
        html.P("End-Time"),
        dcc.Dropdown(id='end_time', options=[
                {'label': 'Today', 'value': 'today'}
            ],
            value='today')
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
    dcc.Graph(id='my-graph'),

    # html.Div([
    #     html.P('Latest NEWS about ~~~~~')
    #     # html.P(news.)
    #     # html.P('Latest NEWS about ~~~~~'),
    #     # html.P(newsapi.print_newsapi())
    # ])

    html.Div(id='update_news')
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    [
        Input(component_id='my-dropdown', component_property='value'),
        Input(component_id='start_time', component_property='value'),
        Input(component_id='end_time', component_property='value')
    ]
    )
def update_graph(selected_dropdown_value, start_time, end_time):
    # print('--- User selected selected_dropdown_value : ', selected_dropdown_value)
    # print('--- User selected start_time : ', start_time)
    # print('--- User selected end_time : ', end_time)
    # TODO : Add a button which will be clicked only when all three options : Stock, start_time and end_time are selected. Graph should be displayed only after this
    # TODO : Validate start_time and end_time
    today_date = datetime.date.today()
    if start_time == 'last_6_mnths':
        start = today_date - datetime.timedelta(6 * 365 / 12)
    elif start_time == 'last_1_yr':
        start = today_date - datetime.timedelta(12 * 365 / 12)
    elif start_time == 'last_5_yrs':
        start = today_date - datetime.timedelta(12 * 5 * 365 / 12)
    else:
        start = today_date - datetime.timedelta(12*365/12)

    if end_time == 'today':
        end = datetime.date.today()
    else:
        end = datetime.date.today()

    # start = datetime.datetime(2018, 1, 1)
    print('start : ', start)
    print('end : ', end)
    df = pdr.get_data_yahoo(selected_dropdown_value, start, end)
    #update_news(selected_dropdown_value)
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }]
    }

"""
Another callback for displaying latest news for each selection
Refer : 'Multiple Outputs' section at https://dash.plot.ly/getting-started-part-2
"""
@app.callback(
    dash.dependencies.Output('update_news', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
    )
def update_news(selected_dropdown_value):
    # TODO : display News on selected company
    # TODO : display Crunchbase updates for the selected company
    company = '{} company'.format(selected_dropdown_value)
    news = newsapi.newsApi('everything', company)
    all_news = news.get_response()
    formated_news = '-------- Checkout the latest news on {} --------  \n'.format(selected_dropdown_value)
    if all_news["status"] == "ok":
        for each_article in all_news["articles"]:
            formated_news += each_article['description'] + "\n\tFor more details visit : " + each_article['url'] + "\n\n"

    # print(formated_news)
    return formated_news
    # return '-------- Checkout the latest news on {} --------  \n'.format(selected_dropdown_value) + all_news['articles'][0]['description'] + '\n\t' + all_news['articles'][0]['url'] + '\n'


# TODO : Create separate methods to calculate start_time and end_time

if __name__ == '__main__':
    crunchbase.print_crunchbase()
    app.run_server(host='127.0.0.1', port=8888)


"""
Python Dash documentation :
    https://dash.plot.ly/getting-started
    
"""