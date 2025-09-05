#!/bin/bash

# Deploy Docker Hub image to Google Cloud Run
# Usage:
#   ./deploy-cloudrun.sh \
#     --project YOUR_PROJECT_ID \
#     --region YOUR_REGION \
#     --service fia-axcelerate-mcp \
#     --image docker.io/mariojoseg/fia-axcelerate-mcp-server:latest \
#     [--env-file env.yaml] \
#     [--allow-unauthenticated]
#
# Example env.yaml:
# AXCELERATE_BASE_URL: "..."
# AXCELERATE_WSTOKEN: "..."
# AXCELERATE_APITOKEN: "..."
# AZURE_API_MODEL: "..."
# AZURE_API_KEY: "..."
# AZURE_API_BASE: "..."
# AZURE_API_VERSION: "..."
# OPENAI_API_KEY: "..."

set -euo pipefail

PROJECT="optical-net-469506-a3"
REGION="us-central1"
SERVICE="fia-axcelerate-mcp"
IMAGE="docker.io/mariojoseg/fia-axcelerate-mcp-server:latest"
ENV_FILE="env.yaml"
ALLOW_UNAUTH=false
MEMORY="512Mi"
CPU="1"
MIN_INSTANCES="0"
MAX_INSTANCES="10"
PORT="8080"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --service) SERVICE="$2"; shift 2 ;;
    --image) IMAGE="$2"; shift 2 ;;
    --env-file) ENV_FILE="$2"; shift 2 ;;
    --allow-unauthenticated) ALLOW_UNAUTH=true; shift ;;
    --memory) MEMORY="$2"; shift 2 ;;
    --cpu) CPU="$2"; shift 2 ;;
    --min-instances) MIN_INSTANCES="$2"; shift 2 ;;
    --max-instances) MAX_INSTANCES="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$PROJECT" || -z "$REGION" ]]; then
  echo "Error: --project and --region are required"
  exit 1
fi

# Configure gcloud
gcloud config set project "$PROJECT" | cat
gcloud config set run/region "$REGION" | cat

echo "Ensuring Cloud Run API is enabled..."
gcloud services enable run.googleapis.com | cat

DEPLOY_CMD=(
  gcloud run deploy "$SERVICE"
  --image="$IMAGE"
  --platform=managed
  --port="$PORT"
  --memory="$MEMORY"
  --cpu="$CPU"
  --min-instances="$MIN_INSTANCES"
  --max-instances="$MAX_INSTANCES"
)

if [[ "$ALLOW_UNAUTH" == true ]]; then
  DEPLOY_CMD+=(--allow-unauthenticated)
fi

if [[ -n "$ENV_FILE" ]]; then
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "Env file not found: $ENV_FILE"; exit 1
  fi
  DEPLOY_CMD+=(--env-vars-file="$ENV_FILE")
else
  echo "No --env-file provided. You can set env vars later with:"
  echo "  gcloud run services update $SERVICE --update-env-vars KEY=VALUE"
fi

set -x
"${DEPLOY_CMD[@]}"
set +x

URL=$(gcloud run services describe "$SERVICE" --format='value(status.url)')
echo "\nDeployed: $URL"
echo "Health check:"
echo "  curl $URL/health"
