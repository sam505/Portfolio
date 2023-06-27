# build
gcloud builds submit --tag gcr.io/feisty-mechanic-389020/samuel-maina --project=feisty-mechanic-389020

# deploy
gcloud run deploy --image gcr.io/feisty-mechanic-389020/samuel-maina --platform managed --project=feisty-mechanic-389020 --allow-unauthenticated