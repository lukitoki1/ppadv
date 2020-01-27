import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objects as go
import pandas as pd
from datetime import timedelta

plot_margin_style = dict(l=20, r=20, t=0, b=20)
plot_legend_style = dict(x=0, y=-0.3, bordercolor="lightgray", borderwidth=1, orientation='h')
plot_font_style = dict(family='Roboto', size=15)

sensor_parameters = {
    0: {'place': 'front', 'side': 'left', 'sign': 'L1'},
    1: {'place': 'middle', 'side': 'left', 'sign': 'L2'},
    2: {'place': 'back', 'side': 'left', 'sign': 'L3'},
    3: {'place': 'front', 'side': 'right', 'sign': 'R1'},
    4: {'place': 'middle', 'side': 'right', 'sign': 'R2'},
    5: {'place': 'back', 'side': 'right', 'sign': 'R3'},
}


def row_col_wrapper(component):
    return dbc.Row(dbc.Col(component))


def plot_layout():
    return [
        row_col_wrapper(html.H3('Recent Readings')),
        row_col_wrapper(dcc.Graph(id='plot')),
        dbc.Row([dbc.Col(
            html.Button('||', id='pause_button'), width=1),
            dbc.Col(
                dcc.RadioItems(
                    id='time_window_buttons',
                    options=[
                        {'label': '30 seconds', 'value': 0.5},
                        {'label': '2 minutes', 'value': 2},
                        {'label': '5 minutes', 'value': 5},
                        {'label': '10 minutes', 'value': 10}
                    ],
                    value=2,
                    labelStyle={'display': 'inline-block', 'family': 'Roboto', 'size': '15', 'padding': '10px'},
                ))
        ], style={'marginTop': '4vh', 'marginLeft': '8vh'})
    ]


def plot(sensor_values: pd.DataFrame, value):
    fig = go.Figure()
    timestamp = sensor_values['timestamp'] + timedelta(hours=1)
    columns = list(sensor_values.columns)
    columns.remove('timestamp')
    for column in columns:
        sensor_parameter = sensor_parameters[column]
        fig.add_trace(
            go.Scatter(x=timestamp, y=sensor_values[column], line_shape='spline',
                       name='{} {}'.format(sensor_parameter['side'].capitalize(),
                                           sensor_parameter['place'].capitalize())))
    fig.update_layout(xaxis_title='Time', yaxis_title='Pressure', margin=plot_margin_style, legend=plot_legend_style,
                      font=plot_font_style, uirevision=f'{value}')
    return fig
