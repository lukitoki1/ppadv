import dash_bootstrap_components as dbc
from colour import Color


external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
patients_ids = ['1', '2', '3', '4', '5', '6']
default_id = '1'
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

sensor_parameters = {
    0: {'place': 'front', 'side': 'left', 'sign': 'L1'},
    1: {'place': 'middle', 'side': 'left', 'sign': 'L2'},
    2: {'place': 'back', 'side': 'left', 'sign': 'L3'},
    3: {'place': 'front', 'side': 'right', 'sign': 'R1'},
    4: {'place': 'middle', 'side': 'right', 'sign': 'R2'},
    5: {'place': 'back', 'side': 'right', 'sign': 'R3'},
}

anomaly_color = Color("red")
no_anomaly_color = Color("green")
