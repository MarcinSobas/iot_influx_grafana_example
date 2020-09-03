#!/usr/bin/env python3

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

client.create_database('example')

json_body = [{
    "measurement": "cpu_load_short",
    "tags": {
        "host": "server01",
        "region": "us-west"
    },
    "time": "2020-01-10T12:00:00Z",
    "fields": {
        "value": 1.0
    }
}]
#
# client.write_points(json_body)
result = client.query('select value, time from cpu_load_short;')
print("Result: {0}".format(result))
