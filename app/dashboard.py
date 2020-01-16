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
        self.app.layout = layout.layout(patients.patients)
        self.add_callbacks()

    def add_callbacks(self):
        @self.app.callback([
            Output('name', 'children'),
            Output('birthday', 'children'),
            Output('disabled', 'children'),
            Output('case', 'children')
        ], [
            Input('dropdown', 'value'),
            Input('interval', 'n_intervals')
        ])
        def switch_patient(value, _):
            patient = list(filter(lambda x: x.id == value, patients.patients))[0]
            return (
                patient.name,
                patient.birthday,
                values.disabled_classification[patient.disabled],
                patient.case
            )


if __name__ == '__main__':
    wrapper = AppWrapper()
    wrapper.app.run_server(port=8000)
