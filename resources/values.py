import dash_bootstrap_components as dbc


external_stylesheets = [dbc.themes.GRID, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
patients_ids = ['1', '2', '3', '4', '5', '6']
base_url = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/'

buffer_time_minutes = 10
data_update_interval_seconds = 1

data_prefix = 'data_'
anomaly_prefix = 'anomaly_'

disabled_classification = {
    True: 'Tak',
    False: 'Nie'
}

name_literal = 'Imię'
birthday_literal = 'Urodziny'
disabled_literal = 'Niepełnosprawny'
case_literal = 'Przypadek'
