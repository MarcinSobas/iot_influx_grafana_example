#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import json
from random import uniform
import datetime as dtime

DEVICE_ID = "rpi_1"
DEVICE_INFO_TOPIC = f"device/{DEVICE_ID}/info"

BROKER_HOST = "0.0.0.0"
BROKER_PORT = 1883

# utworzenie instancji klienta
client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()

# pętla odczytu i publikacji danych
while True:
    data = {
        "timestamp": dtime.datetime.now().isoformat(),
        "data": {
            "utilization": {
                "cpu": uniform(0.0, 100.0),
                "ram": uniform(0.0, 100.0)
            },
            "temperature": uniform(-20.0, 120.0)
        },
    }

    client.publish(DEVICE_INFO_TOPIC, json.dumps(data))
    time.sleep(1)
