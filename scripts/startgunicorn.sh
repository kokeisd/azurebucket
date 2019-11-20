#!/bin/bash
#DJANGO_PROJECT_ROOT=/home/mladmin/kelvinko/git-projects/azurebucket/
source ${DJANGO_PROJECT_ROOT}/.django_env
cd ${DJANGO_PROJECT_ROOT}
export numofcores=`grep -c ^processor /proc/cpuinfo`
export numofworkers=`expr $numofcores \* 2 + 1`
gunicorn  --workers ${numofworkers} -b 0.0.0.0:8000 azurebucket.wsgi:application
#${DJANGO_PROJECT_ROOT}/venv/bin/gunicorn  --workers ${numofworkers} -b 0.0.0.0:8000 azurebucket.wsgi:application
# ${DJANGO_PROJECT_ROOT}/venv/bin/gunicorn  --workers ${numofworkers} -b 0.0.0.0:8000 azurebucket.wsgi:application
