from dash.dependencies import Input, Output
import dash

from app.data import Patients
from resources import values, layout

patients = Patients()


class AppWrapper:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=values.external_stylesheets)
        self.configure_app()

    def configure_app(self):
        self.app.layout = layout.layout(patients.transfer_for_dropdown())
        self.add_callbacks()

    def add_callbacks(self):
        @self.app.callback(
            [
                Output('patient_info', 'children'),
                Output('datatable', 'data')
            ],
            [
                Input('dropdown', 'value'),
                Input('interval', 'n_intervals')
            ])
        def switch_patient(value, _):
            patient = patients.get_patient_by_id(value)
            if patient:
                return layout.patient_info(patient), patient.transfer_for_datatable()
            return [], None


if __name__ == '__main__':
    wrapper = AppWrapper()
    wrapper.app.run_server(port=8000)
