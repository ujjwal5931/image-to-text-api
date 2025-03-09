#!/bin/bash

# Set your Google Cloud project ID
PROJECT_ID="your-project-id"  # Replace with your actual project ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Build and push the container
echo "Building and pushing container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/image-to-text-api

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy image-to-text-api \
  --image gcr.io/$PROJECT_ID/image-to-text-api \
  --platform managed \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --concurrency 10 \
  --allow-unauthenticated \
  --region us-central1

# Get the service URL
echo "Deployment complete. Service URL:"
gcloud run services describe image-to-text-api --platform managed --region us-central1 --format 'value(status.url)' 