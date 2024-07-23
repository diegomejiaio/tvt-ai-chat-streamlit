#!/bin/bash

# Cargar variables del archivo .env
export $(grep -v '^#' .env | xargs)

# Autenticarse con Google Cloud usando la clave de servicio
gcloud auth activate-service-account --key-file="$GCP_SA_KEY_PATH"

# Crear el repositorio de artefactos si no existe
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=docker || true

# Establecer la clave de API de OpenAI como una variable de entorno
export OPENAI_API_KEY=$(grep 'OPENAI_API_KEY' .env | cut -d '=' -f2)

# Ejecutar Cloud Build utilizando el archivo cloudbuild.yaml
gcloud builds submit --config cloudbuild.yaml --substitutions=_GCP_REGION=$GCP_REGION,_GCP_PROJECT=$GCP_PROJECT,_AR_REPO=$AR_REPO,_SERVICE_NAME=$SERVICE_NAME,_OPENAI_API_KEY=$OPENAI_API_KEY

# Desplegar la imagen Docker en Cloud Run con límites para mantener la capa gratuita
gcloud run deploy "$SERVICE_NAME" \
    --port=8080 \
    --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
    --allow-unauthenticated \
    --region="$GCP_REGION" \
    --platform=managed \
    --project="$GCP_PROJECT" \
    --set-env-vars=GCP_PROJECT="$GCP_PROJECT",GCP_REGION="$GCP_REGION",AR_REPO="$AR_REPO",SERVICE_NAME="$SERVICE_NAME",OPENAI_API_KEY="$OPENAI_API_KEY",GCP_SA_KEY_PATH="$GCP_SA_KEY_PATH" \
    --max-instances=1 \
    --concurrency=20 \
    --cpu=2 \
    --memory=1Gi \
    --timeout=300s

# Configurar política IAM para permitir a todos los usuarios invocar el servicio de Cloud Run
# gcloud beta run services add-iam-policy-binding "$SERVICE_NAME" \
#     --region="$GCP_REGION" \
#     --member="allUsers" \
#     --role="roles/run.invoker"

echo "Resources have been provisioned successfully."