#!/bin/sh

docker_ip() {
  docker inspect --format '{{ .NetworkSettings.IPAddress }}' "$@"
}

docker build -t file-service:latest ./components/file_service
docker run -d -p 5000:5000 file-service:latest
echo Minifilebox running at http://0.0.0.0:5000/minifileboc/api/v1

