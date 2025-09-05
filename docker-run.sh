#!/bin/bash

# Docker run script for FIA Axcelerate MCP Server
# Usage: ./docker-run.sh [tag]

set -e

# Configuration
DOCKER_USERNAME="mariojoseg"
IMAGE_NAME="fia-axcelerate-mcp-server"
DEFAULT_TAG="latest"

# Get tag from argument or use default
TAG=${1:-$DEFAULT_TAG}
FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "Running Docker container: ${FULL_IMAGE_NAME}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create one based on env.example"
    echo "Running without environment file..."
    docker run -p 8080:8080 "${FULL_IMAGE_NAME}"
else
    echo "Using .env file for environment variables"
    docker run -p 8080:8080 --env-file .env "${FULL_IMAGE_NAME}"
fi
