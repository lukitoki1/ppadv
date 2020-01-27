import dash_html_components as html
import dash_bootstrap_components as dbc
import itertools
import dash_table

datatable_cell_style = {'height': '14vh', 'width': '5vw', 'fontFamily': 'Roboto', 'fontSize': '100%', 'textAlign': 'left', 'padding': '1vh'}


def row_col_wrapper(component):
    return dbc.Row(dbc.Col(component))


def datatable_layout():
    return [
        row_col_wrapper(html.H3('Live Readings', style={'marginLeft': '0'})),
        row_col_wrapper(dash_table.DataTable(
            id='datatable',
            columns=[{'name': column.split('_')[-1].capitalize(), 'id': column} for column in
                     ['sensor', 'value_left', 'value_right']],
            data=[],
            style_cell=datatable_cell_style,
            style_data_conditional=datatable_conditional_styling(),
        ))]


def datatable_conditional_styling():
    style = []
    for column_id_side, anomaly in itertools.product(['left', 'right'], [True, False]):
        style.append({
            'if': {
                'column_id': f'value_{column_id_side}',
                'filter_query': '{anomaly_%s} eq %s' % (column_id_side, str(anomaly))
            },
            'backgroundColor': '#ff6666' if anomaly else '#42d756',
            'color': 'white'
        })
    return style
