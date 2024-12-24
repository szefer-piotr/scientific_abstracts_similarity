#!/bin/bash

set -euo pipefail

REDIS_IMAGE="redis:7.2"
HOST="127.0.0.1"
PORT=6379

echo "Pulling $REDIS_IMAGE"
docker pull "$REDIS_IMAGE"
echo "$REDIS_IMAGE successfully pulled"

echo "Checking if anything is already running on port $HOST:$PORT"
container_id=$(docker ps -f "expose=$PORT" --format "{{.ID}}")
if [[ -n "$container_id" ]]
then
    echo "$HOST:$PORT is already in use by container $container_id - killing it."
    docker kill "$container_id"
else
    echo "Nothing is running on $HOST:$PORT"
fi

echo "Running $REDIS_IMAGE on $HOST:$PORT"
redis_container_id=$(docker run \
    -v "$(pwd)"/configs/redis/redis.conf:/usr/local/etc/redis/redis.conf:ro \
    -d \
    -p $PORT:$PORT \
    "$REDIS_IMAGE" \
    redis-server /usr/local/etc/redis/redis.conf)

echo "Waitig five seconds for Redis to start"
sleep 5

echo "Checking if we can connect to redis on $HOST:$PORT"
response=$(docker exec -it "$redis_container_id" redis-cli -h $HOST -p $PORT ping)
response=$(echo "$response" | tr -d '\r')
echo "Response: $response"
if [[ "$response" == "PONG" ]] 
then
    echo "Successfully connected to Redis on $HOST:$PORT"
else
    echo "Failed to connect to Redis on $HOST:$PORT"
    echo "Killing the container $redis_container_id"
    exit 1
fi

echo "Everything is ready to go! Redis is listening on $HOST:$PORT"
