import threading
import time
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from requests import HTTPError
import redis
import pickle

START_TIME = time.time()
PATIENTS_IDS = ['1', '2', '3', '4', '5', '6']
BASE_URL = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/'
MAX_BUFFER_MINUTES = 10
UPDATE_INTERVAL_SECONDS = 1

r = redis.Redis(host='localhost', port=6379, db=0)


class Patients:
    def __init__(self):
        self.patients = [Patient(id) for id in PATIENTS_IDS]
        self.update_periodically()

    def update_periodically(self):
        # print('updating data ' + datetime.utcnow().isoformat())
        self.update()
        threading.Timer(
            UPDATE_INTERVAL_SECONDS - ((time.time() - START_TIME) % UPDATE_INTERVAL_SECONDS),
            self.update_periodically
        ).start()

    def update(self):
        for patient in self.patients:
            patient.update()

    def transfer_for_dropdown(self) -> list:
        return [{'label': patient.name, 'value': patient.id} for patient in self.patients]

    def get_patient_by_id(self, id):
        patient = list(filter(lambda patient: patient.id == id, self.patients))
        try:
            return patient[0]
        except IndexError:
            return None

    def __str__(self):
        return '\n'.join([str(patient) for patient in self.patients])


class Patient:
    def __init__(self, id):
        self.id = id

        self.name = None
        self.birthday = None
        self.disabled = None
        self.case = None

        self.data_headers = None

        self.update()

    def update(self):
        data = self._fetch()
        if not data:
            return

        self._update_patient_info(data)

        if self.data_headers is None:
            self._init_data_frames(data)

        timestamp = datetime.utcnow()
        data = data['trace']['sensors']
        values_data = [sensor['value'] for sensor in data]
        anomalies_data = [sensor['anomaly'] for sensor in data]
        self._update_database(timestamp, values_data, anomalies_data)

    def map_for_plot(self, minutes=MAX_BUFFER_MINUTES):
        data = [pickle.loads(e) for e in r.lrange(f'values_{self.id}', 0, -1)]
        data_frame = self.data_headers
        for row in data:
            if row[0] < datetime.utcnow() - timedelta(hours=0, minutes=minutes):
                break
            series = pd.Series(row, index=self.data_headers.columns)
            data_frame = data_frame.append(series, ignore_index=True)
        return data_frame

    def map_for_datatable(self) -> list:
        return [self.__map_for_datatable_util_fun('Front', 1, 4),
                self.__map_for_datatable_util_fun('Middle', 2, 5),
                self.__map_for_datatable_util_fun('Back', 3, 6)]

    def __map_for_datatable_util_fun(self, sensor, left_foot_column_name, right_foot_column_name):
        value_data = pickle.loads(r.lrange(f'values_{self.id}', 0, 0)[0])
        anomaly_data = pickle.loads(r.lrange(f'anomalies_{self.id}', 0, 0)[0])
        return {
            'sensor': sensor,
            'value_left': value_data[left_foot_column_name],
            'value_right': value_data[right_foot_column_name],
            'anomaly_left': str(anomaly_data[left_foot_column_name]),
            'anomaly_right': str(anomaly_data[right_foot_column_name])
        }

    def _fetch(self) -> dict:
        try:
            data = requests.get(f'{BASE_URL}{self.id}')
            return json.loads(data.content)
        except HTTPError:
            return {}

    def _init_data_frames(self, data):
        df_columns = ['timestamp'] + [sensor['id'] for sensor in data['trace']['sensors']]
        self.data_headers = pd.DataFrame(columns=df_columns)

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
            data_frame['timestamp'] > timestamp - timedelta(hours=0, minutes=MAX_BUFFER_MINUTES)]
        return data_frame

    def _update_database(self, timestamp, values_data, anomalies_data):
        val_stamp, anom_stamp = [timestamp], [timestamp]
        for value, anomaly in zip(values_data, anomalies_data):
            val_stamp.append(value)
            anom_stamp.append(anomaly)
        r.lpush(f'values_{self.id}', pickle.dumps(val_stamp))
        r.lpush(f'anomalies_{self.id}', pickle.dumps(anom_stamp))

        first_values = r.rpop(f'values_{self.id}')
        first_anomalies = r.rpop(f'anomalies_{self.id}')
        first_timestamp = pickle.loads(first_values)[0]
        while first_timestamp < timestamp - timedelta(hours=0, minutes=MAX_BUFFER_MINUTES):
            first_values = r.rpop(f'values_{self.id}')
            first_anomalies = r.rpop(f'anomalies_{self.id}')
            first_timestamp = pickle.loads(first_values)[0]
        r.rpush(f'values_{self.id}', first_values)
        r.rpush(f'anomalies_{self.id}', first_anomalies)
