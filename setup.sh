#!/usr/bin/env bash

docker-compose -f "docker-compose.yml" down
# pipenv install
sudo rm -r grafana

mkdir grafana
mkdir grafana/data
mkdir grafana/provisioning
mkdir grafana/provisioning/datasources
cp datasource.yml grafana/provisioning/datasources

sudo chown -R 472:472 grafana
sudo chown -R 0:0 grafana/provisioning

docker-compose -f "docker-compose.yml" up -d --build