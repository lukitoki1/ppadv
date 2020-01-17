import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from resources import values


def row_col_wrapper(component):
    return dbc.Row(dbc.Col(component))


def card(value, title):
    return dbc.Card([
        dbc.CardHeader(title + ':'),
        dbc.CardBody(html.H4(value, className="card-title"))
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
        data=[]
    )


plot = None


def layout(patients_list: list):
    return html.Div([
        dcc.Interval(id='interval', interval=values.data_update_interval_seconds * 1000),
        dbc.Container([
            dbc.Row([
                dbc.Col(patient_overview(patients_list), width=3),
                dbc.Col(datatable(), width=3),
                dbc.Col(plot, width=6),
            ])
        ],
            fluid=True,
        )
    ])
