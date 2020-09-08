#!/usr/bin/env bash
#
# zadania wykonywane przez skrypt
# - konifiguracja środowiska dla serwisów Docker Compose
# - uruchomienie serwisów

# zatrzymanie serwisów
docker-compose -f "docker-compose.yml" down

#-------------------- konfiguracja dla serwisu grafana
mkdir -p .env/grafana/provisioning/datasources
# umieszczenie konfiguracji źródła danych w zasobie współdzielonym przez serwis
cp config/grafana/datasource.yml .env/grafana/provisioning/datasources
# modyfikacja użotkownika/grupy katalogów wymagana przez serwis
sudo chown -R 472:472 .env/grafana
sudo chown -R 0:0 .env/grafana/provisioning
#--------------------

# uruchomienie serwisów
docker-compose -f "docker-compose.yml" up -d --build