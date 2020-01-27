import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash

from data import Patients
from layout import layout, plot_layout, info_layout

EXTERNAL = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css',
            'https://fonts.googleapis.com/css?family=Roboto&display=swap']


def button_pressed(n_clicks):
    if n_clicks is None or n_clicks % 2 == 0:
        return False
    return True



class AppWrapper:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=EXTERNAL)
        self.patients = Patients()
        self.configure_app()

    def configure_app(self):
        self.app.layout = layout.layout(self.patients.transfer_for_dropdown())
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
            patient = self.patients.get_patient_by_id(value)
            if patient:
                return (info_layout.patient_info(patient),
                        patient.map_for_datatable())
            return [], None

        @self.app.callback(
            Output('interval', 'disabled'),
            [Input('pause_button', 'n_clicks')]
        )
        def pause_resume(n_clicks):
            return button_pressed(n_clicks)

        @self.app.callback(
            Output('plot', 'figure'),
            [
                Input('dropdown', 'value'),
                Input('interval', 'n_intervals'),
                Input('time_window_buttons', 'value'),
            ])
        def display_plot(value, _, time_window):
            patient = self.patients.get_patient_by_id(value)
            if not patient:
                return None
            return plot_layout.plot(patient.map_for_plot(time_window), value)


if __name__ == '__main__':
    wrapper = AppWrapper()
    wrapper.app.run_server(port=8000)
