#!/bin/bash
#printenv > /code/scripts/.cron_env
# cronfile=/etc/cron.d/cron
cronfile=/etc/crontabs/root 
cat /dev/null > $cronfile
printenv |grep -v CRON_| sed 's/^\(.*\)$/export \1/g' > /code/scripts/.cron_env
echo "SHELL=/bin/bash" >> $cronfile
echo "BASH_ENV=/code/scripts/.cron_env" >> $cronfile

for cronvar in ${!CRON_*}; do
	cronvalue=${!cronvar}
	echo "Installing $cronvar"
	echo "$cronvalue >> /dev/stdout 2>&1" >> $cronfile
done
echo >> $cronfile # Newline is required
crontab $cronfile



