docker stop azurebucket*
docker rm azurebucket*
docker build -t  azurebucket-web:v0.1.1 . -f Dockerfile.web
docker build -t  azurebucket-cron:v0.1.1 . -f Dockerfile.cron