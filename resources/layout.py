import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from resources import values


def patients_to_dropdown_list(patients: list):
    return [{'label': patient.name, 'value': patient.id} for patient in patients]


def row_col_wrapper(component):
    return dbc.Row(dbc.Col(component))


def card(id, title):
    return dbc.Card([
        dbc.CardHeader(title + ':'),
        dbc.CardBody(html.H4('', className="card-title", id=id))
    ])


def patient_overview(patients):
    return [
        row_col_wrapper(dcc.Dropdown(id='dropdown', options=patients_to_dropdown_list(patients))),
        row_col_wrapper(card('name', values.name_literal)),
        row_col_wrapper(card('birthday', values.birthday_literal)),
        row_col_wrapper(card('disabled', values.disabled_literal)),
        row_col_wrapper(card('case', values.case_literal))
    ]


datatable = None

plot = None


def layout(patients):
    return html.Div([
        dcc.Interval(id='interval', interval=values.data_update_interval_seconds * 1000),
        dbc.Container([
            dbc.Row([
                dbc.Col(patient_overview(patients), width=3),
                dbc.Col(datatable, width=3),
                dbc.Col(plot, width=6),
            ])
        ],
            fluid=True,
        )
    ])
