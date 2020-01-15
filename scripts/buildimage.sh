docker kill $(docker ps -aqf name='azurebucket')
docker rm $(docker ps -aqf name='azurebucket')
docker build -t  azurebucket-web:v0.1.3 . -f Dockerfile.web
docker build -t  azurebucket-cron:v0.1.3 . -f Dockerfile.cron