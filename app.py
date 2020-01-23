import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash

from data import Patients
from layout import layout, plot_layout, info_layout

EXTERNAL = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css',
            'https://fonts.googleapis.com/css?family=Roboto&display=swap']

patients = Patients()


class AppWrapper:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=EXTERNAL)
        self.configure_app()

    def configure_app(self):
        self.app.layout = layout.layout(patients.transfer_for_dropdown())
        self.add_callbacks()

    def add_callbacks(self):
        @self.app.callback(
            [
                Output('patient_info', 'children'),
                Output('datatable', 'data'),
                Output('plot', 'figure')
            ],
            [
                Input('dropdown', 'value'),
                Input('interval', 'n_intervals')
            ])
        def switch_patient(value, _):
            patient = patients.get_patient_by_id(value)
            if patient:
                return (info_layout.patient_info(patient),
                        patient.transfer_for_datatable(),
                        plot_layout.plot(patient))
            return [], None


if __name__ == '__main__':
    wrapper = AppWrapper()
    wrapper.app.run_server(port=8000)
