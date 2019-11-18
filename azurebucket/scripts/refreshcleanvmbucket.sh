#!/bin/bash
(
ISRUNNING=`ps -ef |grep -v grep |grep -i 'loadvmbucket.py'|wc -l`
#output=`ps -ef |grep -v grep |grep -i 'loadvmbucket.py\|refreshvmbucket.sh'`
if  [ $ISRUNNING -gt 0 ]
then
    echo "Process already running"
    exit 1
fi

source /app/djangoprojects/bucketapi/venv/bin/activate
cd /app/djangoprojects/bucketapi/scripts
python cleanvmbucket.py
python resetvmkucketseq.py
python loadvmbucket.py 2>&1) |tee -a  /app/djangoprojects/bucketapi/scripts/logs/loadvmbucket.`date +%Y%m%d%H%M%S`.log
