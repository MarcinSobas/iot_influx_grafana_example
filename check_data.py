#!/usr/bin/env python3

from influxdb import InfluxDBClient

DB_HOST = "localhost"
DB_PORT = 8086
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "io_device_info"

db_client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
db_client.create_database(DB_NAME)

# result = db_client.query(
# 'SELECT temperature FROM device_temperature WHERE time >= now() - 6h ')
#
# result = db_client.query(
#     'SELECT mean("cpu") FROM "device_utilization" WHERE time >= now() - 6h GROUP BY time(15s) fill(null)'
# )

# result = db_client.query(
# 'SELECT mean("cpu") FROM "device_utilization" WHERE time >= now() - 10m GROUP BY time(2s) fill(null)'
# )

result = db_client.query(
    'SELECT mean("temperature") FROM "device_temperature" WHERE time >= now() - 10m GROUP BY time(2s) fill(null)'
)

print("Result: {0}".format(result))