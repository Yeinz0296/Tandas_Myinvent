from dash import dash, html, dcc, Output, Input
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
from plotly import express as px
from datetime import datetime as dt


app = dash.Dash(__name__, requests_pathname_prefix="/perempuan/", title='Penggunaan Air Tandas Perempuan',external_stylesheets=[dbc.themes.LUX])
app.title = "Penggunaan Air Tandas Perempuan"

app.layout = html.Div(
    
    children=[
    html.H1(children='Monitor Penggunaan Air Tandas Perempuan by Hazrien Nazman'),

    html.Div(children='''
    REAL IME DATA MONITORING SYSTEM
    '''),
    
    # GRAPH SECTION
    html.Div(
        children=[
        # dcc.Dropdown(
        # ['Temperature','Humidity'],
        # 'Temperature',
        # id='dropdown'),
        dcc.Graph(id='TvT'),
        ]
    ),
    
    html.Div(
        children=[
        daq.Gauge(
            id='TemperatureGauge',
            showCurrentValue=True,
            label="Tandas Perempuan",
            value=35,
            max=10,
            min=0
        ),
        
        ],
        style={'width': '49%', 'display': 'inline-block'}
    ),

    # html.Div(
    #     children=[
    #         daq.Gauge(
    #         id='TemperatureHumidity',
    #         showCurrentValue=True,
    #         label="Temperature Humidity",
    #         value=50,
    #         max=100,
    #         min=0
    #     ),
    #     ],
    #     style={'width': '49%', 'display': 'inline-block'}
    # ),

    #Auto Refresh
    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
    )
])

@app.callback(
    Output('TvT','figure'),
    Input('interval-component', 'n_intervals'),
    )
def update_graph(interval):
    dataframe = pd.read_csv("tandas.csv")
    timestamp = dataframe['Timestamp']
    dataframe['Dates'] = pd.to_datetime(timestamp).dt.date 
    dataframe['Time'] = pd.to_datetime(timestamp).dt.time
    date_specify = dataframe[dataframe["Dates"]==dt.today().date()]

    fig = px.line(date_specify, x='Time', y='Total', title='Total vs time')
    return fig

@app.callback(
    Output('TemperatureGauge','value'),
    Input('interval-component', 'n_intervals'))
def update_gauge_temperature(value):
    dataframe = pd.read_csv("tandas.csv")
    value = dataframe['Total'].iloc[-1]
    return value

# @app.callback(
#     Output('TemperatureHumidity','value'),
#     Input('interval-component', 'n_intervals'))
# def update_gauge_humidity(value):
#     dataframe = pd.read_csv("fastdata.csv")
#     value = dataframe['Humidity'].iloc[-1]
#     return value
# app.run_server(debug=True, threaded=True)