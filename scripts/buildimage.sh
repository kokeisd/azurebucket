docker stop azurebucket*
docker rm azurebucket*
docker build -t  azurebucket-web:v0.1.0 . -f Dockerfile.web
docker build -t  azurebucket-cron:v0.1.0 . -f Dockerfile.cron

docker run -d -e DJANGO_ENV=DEV \
-e AZURE_TENANT_ID='5d3e2773-e07f-4432-a630-1a0f68a28a05' \
-e AZURE_CLIENT_ID='03828b49-95e3-4856-975f-8e12a6a50a73' \
-e AZURE_CLIENT_SECRET='djd5hzSLRcaK0jTJjl1+xKPGQcRxUXiYDkuB0fq+ZjY=' \
-p 8000:8000 -p 80:80 -p 443:443 --name azurebucket-web   azurebucket-web:v0.1.0


docker run -d -e DJANGO_ENV=DEV \
-e AZURE_TENANT_ID='5d3e2773-e07f-4432-a630-1a0f68a28a05' \
-e AZURE_CLIENT_ID='03828b49-95e3-4856-975f-8e12a6a50a73' \
-e AZURE_CLIENT_SECRET='djd5hzSLRcaK0jTJjl1+xKPGQcRxUXiYDkuB0fq+ZjY=' \
--name azurebucket-cron   azurebucket-cron:v0.1.0
