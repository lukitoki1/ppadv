import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go

from resources import values
from app.data import Patient


def row_col_wrapper(component):
    return dbc.Row(dbc.Col(component))


def card(value, title):
    return dbc.Card([
        dbc.CardHeader(title + ':'),
        dbc.CardBody(html.H6(value, className="card-title"))
    ])


def patient_info(patient):
    return [
        row_col_wrapper(card(patient.name, values.name_literal)),
        row_col_wrapper(card(patient.birthday, values.birthday_literal)),
        row_col_wrapper(card(values.disabled_classification[patient.disabled], values.disabled_literal)),
        row_col_wrapper(card(patient.case, values.case_literal))
    ]


def patient_overview(patients_list: list):
    return [
        row_col_wrapper(dcc.Dropdown(
            id='dropdown',
            options=patients_list,
            value=patients_list[0]['value'],
            clearable=False)
        ),
        html.Div(id='patient_info')
    ]


def datatable():
    return dash_table.DataTable(
        id='datatable',
        columns=[{'name': column, 'id': column} for column in
                 ['sensor', 'value_left', 'value_right']],
        data=[],
        style_cell={'height': '10vh'},
    )


def plot(patient: Patient):
    fig = go.Figure()

    columns = list(patient.sensor_values.columns)
    columns.remove('timestamp')
    for column in columns:
        fig.add_trace(go.Scatter(x=patient.sensor_values['timestamp'], y=patient.sensor_values[column], name=column,
                                 line=dict(color='firebrick')))
    fig.update_layout(xaxis_title='Czas', yaxis_title='Nacisk')
    return fig


def layout(patients_list: list):
    return html.Div([
        dcc.Interval(id='interval', interval=values.data_update_interval_seconds * 1000),
        dbc.Container([
            dbc.Row([
                dbc.Col(patient_overview(patients_list), width=2),
                dbc.Col(datatable(), width=2),
                dbc.Col(dcc.Graph(id='plot'), width=8),
            ])
        ],
            fluid=True,
        )
    ])
