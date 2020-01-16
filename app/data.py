import threading
from time import sleep

import pandas as pd
import requests
import json
from datetime import datetime, timedelta

from requests import HTTPError

from resources import values


class Patients:
    def __init__(self):
        self.patients = [Patient(id) for id in values.patients_ids]
        self.update_periodically()

    def update_periodically(self):
        print('aktualizacja')
        self.update()
        threading.Timer(values.data_update_interval_seconds, self.update_periodically).start()

    def update(self):
        for patient in self.patients:
            patient.update()

    def __str__(self):
        return '\n'.join([str(patient) for patient in self.patients])


class Patient:
    def __init__(self, id):
        self.id = id

        self.name = None
        self.birthday = None
        self.disabled = None
        self.case = None

        self.sensor_values = None
        self.sensor_anomalies = None

        self.update()

    def update(self):
        data = self._fetch()
        if not data:
            return

        self._update_patient_info(data)

        if self.sensor_values is None or self.sensor_anomalies is None:
            self._init_data_frames(data)

        timestamp = datetime.utcnow()
        data = data['trace']['sensors']
        values_data = [sensor['value'] for sensor in data]
        anomalies_data = [sensor['anomaly'] for sensor in data]
        self.sensor_values = self._update_data_frame(timestamp, values_data, self.sensor_values)
        self.sensor_anomalies = self._update_data_frame(timestamp, anomalies_data, self.sensor_anomalies)

    def _fetch(self) -> dict:
        try:
            data = requests.get(f'{values.base_url}{self.id}')
            return json.loads(data.content)
        except HTTPError:
            return {}

    def _init_data_frames(self, data):
        df_columns = ['timestamp'] + [sensor['id'] for sensor in data['trace']['sensors']]
        self.sensor_values = pd.DataFrame(columns=df_columns)
        self.sensor_anomalies = pd.DataFrame(columns=df_columns)

    def _update_patient_info(self, data):
        self.name = f"{data['firstname']} {data['lastname']}"
        self.birthday = data['birthdate']
        self.disabled = data['disabled']
        self.case = data['trace']['name']

    def _update_data_frame(self, timestamp, data, data_frame: pd.DataFrame):
        row = [timestamp]
        for value in data:
            row.append(value)
        series = pd.Series(row, index=data_frame.columns)
        data_frame = data_frame.append(series, ignore_index=True)
        data_frame = data_frame[
            data_frame['timestamp'] > timestamp - timedelta(hours=0, minutes=values.buffer_time_minutes)]
        return data_frame

    def __str__(self):
        return f'{self.id, self.name, self.birthday, self.disabled, self.case}\n{self.sensor_values}\n{self.sensor_anomalies}'


if __name__ == '__main__':
    patients = Patients()
    patients.update()
    patients.update()
    print(patients)