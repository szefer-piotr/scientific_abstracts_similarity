#!/bin/bash

set -euo pipefail

POSTGRES_IMAGE="postgres:15.4"
HOST="127.0.0.1"
PORT="5432"
POSTGRES_PASSWORD="12345"

echo "Pulling $POSTGRES_IMAGE"
docker pull "$POSTGRES_IMAGE"
echo "$POSTGRES_IMAGE pulled successfully"

echo "Checking if postgres container is already running on $HOST:$PORT"
container_id=$(docker ps -f "expose=$PORT" --format "{{.ID}}")
if [[ -n "$container_id" ]]; then
  echo "Postgres container is already running on $HOST:$PORT"
  docker kill "$container_id"
else
    echo "No postgres container is running on $HOST:$PORT"
fi

echo "Running $POSTGRES_IMAGE on $HOST:$PORT"
postgres_container_id=$(docker run -d -p $PORT:$PORT -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" "$POSTGRES_IMAGE")

echo "Waiting for postgres to start"
sleep 5

echo "Checking if we can connect to postgres on $HOST:$PORT"
set +e
response=$(pg_isready --host=$HOST --port=$PORT --username=postgres)
if [[ "$response" == "$HOST:$PORT - accepting connections" ]]; then
  echo "Postgres is running on $HOST:$PORT"
else
  echo "Postgres is not running on $HOST:$PORT"
  exit "$response"
  exit 1
fi

echo "Setting up Postgres"

echo "Creating database and granting permissions"
PGPASSWORD=$POSTGRES_PASSWORD psql -v ON_ERROR_STOP=1 -h $HOST -p $PORT -U postgres -f "$(pwd)/configs/postgres/schemas/databases/monitoring.sql"
if [[ "$?" -eq 0 ]]; then
  echo "Succesfully created database and grant permissions"
else
    echo "Failed to create database and grant permissions"
    docker kill "$postgres_container_id"
    exit "$?"
fi

echo "Creating search result table"
PGPASSWORD=$POSTGRES_PASSWORD psql -v ON_ERROR_STOP=1 -h $HOST -p $PORT -U postgres -d monitoring -f "$(pwd)"/configs/postgres/schemas/tables/search_results.sql
if [ "$?" -eq 0 ]; then
  echo "Successfully created decisions table"
else
  echo "Cannot create decisions table"
  docker kill "$postgres_container_id"
  exit "$?"
fi