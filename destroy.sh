#!/bin/bash

# Cargar variables del archivo .env
export $(grep -v '^#' .env | xargs)

# Eliminar el servicio de Cloud Run
echo "Deleting Cloud Run service..."
gcloud run services delete "$SERVICE_NAME" --region="$GCP_REGION" --platform=managed --quiet

# Eliminar las imágenes en Artifact Registry
echo "Deleting images in Artifact Registry..."
gcloud artifacts repositories delete "$AR_REPO" --location="$GCP_REGION" --quiet

# Eliminar objetos en el bucket de Cloud Storage utilizado por Cloud Build
echo "Deleting objects in Cloud Storage bucket..."
gsutil -m rm -r gs://$GCP_PROJECT\_cloudbuild/source/*

# Eliminar el bucket de Cloud Storage
echo "Deleting Cloud Storage bucket..."
gsutil rb gs://$GCP_PROJECT\_cloudbuild

# Opcional: Eliminar la cuenta de servicio si se creó específicamente para este proyecto
# echo "Deleting service account..."
# gcloud iam service-accounts delete "$SERVICE_ACCOUNT" --quiet

# Confirmar que los recursos han sido eliminados
echo "Resources have been deprovisioned successfully."