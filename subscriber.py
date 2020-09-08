#!/usr/bin/env python3

import json
from abc import ABC, abstractmethod
from influxdb import InfluxDBClient

import paho.mqtt.client as mqtt

BROKER_HOST = "0.0.0.0"
BROKER_PORT = 1883

DB_HOST = "localhost"
DB_PORT = 8086
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "test"


class Observer(ABC):
    @abstractmethod
    def notify(self, data):
        pass


class IoDeviceDataDbWriter(Observer):
    def __init__(self, client):
        self.client = client

    def notify(self, data):
        print(data)
        try:
            self.client.write_points(self._load_points(data))

            # result = self.client.query('select * from device_utilization')
            # print("Result: {0}".format(result))

            # result = self.client.query('select * from device_temperature')
            # print("Result: {0}".format(result))
        except Exception as e:
            print(e)

    def _load_points(self, data):
        device_id = data['device_id']
        timestamp = data['timestamp']
        device_data = data['data']

        return [
            self._load_point(
                measurement="device_utilization",
                host_id=device_id,
                timestamp=timestamp,
                fields=device_data['utilization'],
            ),
            self._load_point(
                measurement="device_temperature",
                host_id=device_id,
                timestamp=timestamp,
                fields={'temperature': device_data['temperature']},
            ),
        ]

    def _load_point(self, measurement, host_id, timestamp, fields):
        return {
            "measurement": measurement,
            "tags": {
                "host": host_id
            },
            "time": timestamp,
            "fields": fields
        }


class IoTDeviceInfoSubScriber:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.observers = []

    def register_new_data_observer(self, observer):
        if not isinstance(observer, Observer):
            TypeError("observer must derive from 'Observer' class ")
        self.observers.append(observer)

    def run(self, host, port=1883):
        self.client.connect(host, port, 60)
        self.client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        self.client.subscribe("device/+/info")

    def _on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        data['device_id'] = msg.topic.split('/')[1]

        for observer in self.observers:
            observer.notify(data)


db_client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
db_client.create_database(DB_NAME)

data_db_writer = IoDeviceDataDbWriter(db_client)

subscriber = IoTDeviceInfoSubScriber()
subscriber.register_new_data_observer(data_db_writer)

subscriber.run(BROKER_HOST, BROKER_PORT)
