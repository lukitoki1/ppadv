import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

disabled_classification = {
    True: 'Yes',
    False: 'No'
}


def row_col_wrapper(component):
    return dbc.Row(dbc.Col(component))


def card(value, title):
    return dbc.Card([
        dbc.CardHeader(title + ':'),
        dbc.CardBody(html.H6(value, className="card-title"))
    ],
        style={'marginBottom': '2vh'}
    )


def patient_info(patient):
    return [
        row_col_wrapper(card(patient.name, "Name")),
        row_col_wrapper(card(patient.birthday, "Birthday")),
        row_col_wrapper(card(disabled_classification[patient.disabled], "Disabled")),
        row_col_wrapper(card(patient.case, "Case"))
    ]


def patient_overview_layout(patients_list: list):
    return [
        row_col_wrapper(html.H3('Personal Info')),
        row_col_wrapper(
            dcc.Dropdown(
                id='dropdown',
                options=patients_list,
                value=patients_list[0]['value'],
                clearable=False,
                style={'marginBottom': '2vh'}
            )),
        html.Div(id='patient_info')
    ]
