#!/bin/bash

source ${DJANGO_PROJECT_ROOT}/scripts/setenv.sh
source ${DJANGO_PROJECT_ROOT}/venv/bin/activate
cd ${DJANGO_PROJECT_ROOT}
gunicorn  --workers ${NUMOFWORKERS} -b 0.0.0.0:${DJANGO_PORT} azurebucket.wsgi:application
#${DJANGO_PROJECT_ROOT}/venv/bin/gunicorn  --workers ${numofworkers} -b 0.0.0.0:8000 azurebucket.wsgi:application
# ${DJANGO_PROJECT_ROOT}/venv/bin/gunicorn  --workers ${numofworkers} -b 0.0.0.0:8000 azurebucket.wsgi:application
