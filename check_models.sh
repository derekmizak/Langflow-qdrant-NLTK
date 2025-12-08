#!/bin/bash

PROJECT_ID="llm-202512"
REGION="us-central1"
TOKEN=$(gcloud auth print-access-token)

check_model() {
  MODEL_ID=$1
  echo "Checking $MODEL_ID..."
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-Goog-User-Project: $PROJECT_ID" \
    "https://$REGION-aiplatform.googleapis.com/v1/publishers/google/models/$MODEL_ID")

  if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ $MODEL_ID is available."
  elif [ "$HTTP_CODE" == "404" ]; then
    echo "❌ $MODEL_ID not found (404)."
  else
    echo "⚠️ $MODEL_ID check failed with code $HTTP_CODE."
  fi
}

echo "Checking availability in $REGION for project $PROJECT_ID..."

check_model "gemini-1.5-pro-001"
check_model "gemini-1.5-flash-001"
check_model "gemini-3-pro-preview"
check_model "gemini-2.5-pro"
check_model "gemini-2.5-flash"


# Control check
REGION_CONTROL="us-central1"
echo "--- Control Check: $REGION_CONTROL ---"
REGION=$REGION_CONTROL
check_model "gemini-1.5-pro"
check_model "gemini-1.5-flash"

