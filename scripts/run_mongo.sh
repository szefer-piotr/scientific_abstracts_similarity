#!/bin/bash

set -euo pipefail

MONGO_IMAGE="mongo:5.0.3"
HOST="127.0.0.1"
PORT="27017"
MONGO_ROOT_PASSWORD="12345"

echo "Pulling $MONGO_IMAGE"
docker pull "$MONGO_IMAGE"
echo "$MONGO_IMAGE pulled successfully"

echo "Checking if MongoDB is running on $HOST:$PORT"
container_id




# CHATGPT: MongoDB Import Script
#!/bin/bash

# Variables
docker_image="mongo"
container_name="mongodb_vector"
mongo_port="27017"
data_file="data.json"  # Update this with your JSON file path
collection_name="vectors" # The collection where data will be imported

echo "Checking if Docker is installed..."
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

echo "Pulling MongoDB Docker image..."
docker pull $docker_image

echo "Starting MongoDB container..."
docker run -d --name $container_name -p $mongo_port:$mongo_port $docker_image

# Wait for MongoDB to initialize
echo "Waiting for MongoDB to initialize..."
sleep 10

echo "Checking if data file exists..."
if [ ! -f "$data_file" ]; then
    echo "Data file $data_file not found! Please provide a valid JSON file."
    docker stop $container_name
    docker rm $container_name
    exit 1
fi

# Import JSON data into MongoDB
echo "Importing data from $data_file into MongoDB collection '$collection_name'..."
docker exec -i $container_name mongoimport --db test --collection $collection_name --file /tmp/$data_file --jsonArray

if [ $? -eq 0 ]; then
    echo "Data imported successfully."
else
    echo "Failed to import data. Check your JSON file format and try again."
fi

# Ensure MongoDB Vector Search prerequisites
# Requires MongoDB 6.0 or higher and additional configuration
echo "Ensure that your MongoDB version and settings are compatible with Atlas Vector Search."

# Cleanup option
echo "To stop and remove the container, run:"
echo "  docker stop $container_name && docker rm $container_name"
