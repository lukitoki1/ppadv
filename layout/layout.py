import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import data
from layout.datatable_layout import datatable
from layout.info_layout import patient_overview


def layout(patients_list: list):
    return html.Div([
        dcc.Interval(id='interval', interval=data.UPDATE_INTERVAL_SECONDS * 1000),
        dbc.Container([
            dbc.Row([
                dbc.Col(patient_overview(patients_list), width=2),
                dbc.Col(datatable(), width=2),
                dbc.Col(dcc.Graph(id='plot'), width=8),
            ])
        ],
            fluid=True,
            style={'padding': '4vh'},
        )
    ])
