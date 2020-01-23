from plotly import graph_objects as go

from data import Patient

margin_style = dict(l=20, r=20, t=0, b=20)
legend_style = dict(x=0, y=-0.3, bordercolor="lightgray", borderwidth=1, orientation='h')
font_style = dict(family='Roboto', size=15)

sensor_parameters = {
    0: {'place': 'front', 'side': 'left', 'sign': 'L1'},
    1: {'place': 'middle', 'side': 'left', 'sign': 'L2'},
    2: {'place': 'back', 'side': 'left', 'sign': 'L3'},
    3: {'place': 'front', 'side': 'right', 'sign': 'R1'},
    4: {'place': 'middle', 'side': 'right', 'sign': 'R2'},
    5: {'place': 'back', 'side': 'right', 'sign': 'R3'},
}


def plot(patient: Patient):
    fig = go.Figure()
    columns = list(patient.sensor_values.columns)
    columns.remove('timestamp')
    for column in columns:
        sensor_parameter = sensor_parameters[column]
        fig.add_trace(go.Scatter(x=patient.sensor_values['timestamp'], y=patient.sensor_values[column],
                                 name='{} {}'.format(sensor_parameter['side'].capitalize(),
                                                     sensor_parameter['place'].capitalize())))
    fig.update_layout(xaxis_title='Time', yaxis_title='Pressure', margin=margin_style,legend=legend_style,
                      font=font_style)
    return fig
