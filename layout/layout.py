import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import data
from layout.datatable_layout import datatable_layout
from layout.info_layout import patient_overview_layout
from layout.plot_layout import plot_layout


def layout(patients_list: list):
    return html.Div([
        dcc.Interval(id='interval', interval=data.UPDATE_INTERVAL_SECONDS * 1000),
        dbc.Container([
            dbc.Row([
                dbc.Col(patient_overview_layout(patients_list), width=2),
                dbc.Col(datatable_layout(), width=2),
                dbc.Col(plot_layout(), width=8),
            ])
        ],
            fluid=True,
            style={'padding': '4vh'},
        )
    ])
