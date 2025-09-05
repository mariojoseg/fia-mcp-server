#!/bin/bash

# Build and push script for FIA Axcelerate MCP Server
# Usage: ./build-and-push.sh [tag]

set -e

# Configuration
DOCKER_USERNAME="mariojoseg"
IMAGE_NAME="fia-axcelerate-mcp-server"
DEFAULT_TAG="latest"

# Get tag from argument or use default
TAG=${1:-$DEFAULT_TAG}
FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "Building and pushing Docker image: ${FULL_IMAGE_NAME}"

# Build the Docker image for amd64 architecture
echo "Building Docker image..."
docker build --platform linux/amd64 -t "${FULL_IMAGE_NAME}" .

# Tag as latest if not already latest
if [ "$TAG" != "latest" ]; then
    LATEST_TAG="${DOCKER_USERNAME}/${IMAGE_NAME}:latest"
    echo "Tagging as latest: ${LATEST_TAG}"
    docker tag "${FULL_IMAGE_NAME}" "${LATEST_TAG}"
fi

# Push the image to Docker Hub
echo "Pushing image to Docker Hub..."
docker push "${FULL_IMAGE_NAME}"

# Push latest tag if it was created
if [ "$TAG" != "latest" ]; then
    echo "Pushing latest tag..."
    docker push "${LATEST_TAG}"
fi

echo "Successfully built and pushed:"
echo "  - ${FULL_IMAGE_NAME}"
if [ "$TAG" != "latest" ]; then
    echo "  - ${LATEST_TAG}"
fi

echo ""
echo "To run the container:"
echo "  docker run -p 8080:8080 --env-file .env ${FULL_IMAGE_NAME}"
