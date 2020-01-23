import itertools

import dash_table


def datatable():
    return dash_table.DataTable(
        id='datatable',
        columns=[{'name': column.split('_')[-1].capitalize(), 'id': column} for column in
                 ['sensor', 'value_left', 'value_right']],
        data=[],
        style_cell={'height': '18.8vh', 'fontFamily': 'Roboto', 'textAlign': 'left', 'padding': '1vh'},
        style_data_conditional=datatable_conditional_styling(),
    )


def datatable_conditional_styling():
    style = []
    for column_id_side, anomaly in itertools.product(['left', 'right'], [True, False]):
        style.append({
            'if': {
                'column_id': f'value_{column_id_side}',
                'filter_query': '{anomaly_%s} eq %s' % (column_id_side, str(anomaly))
            },
            'backgroundColor': '#800000' if anomaly else '#008000',
            'color': 'white'
        })
    return style
