#!/bin/bash
(
ISRUNNING=`ps -ef |grep -v grep |grep -i 'loadvmbucket.py'|wc -l`
if  [ $ISRUNNING -gt 0 ]
then
    echo "Process already running"
    exit 1
fi
source ${DJANGO_PROJECT_ROOT}/scripts/setenv.sh
source ${DJANGO_PROJECT_ROOT}venv/bin/activate
cd ${DJANGO_PROJECT_ROOT}/scripts
python cleanvmbucket.py
python resetvmkucketseq.py
python loadvmbucket.py 2>&1) |tee -a  ${DJANGO_PROJECT_ROOT}/scripts/logs/loadvmbucket.`date +%Y%m%d%H%M%S`.log
