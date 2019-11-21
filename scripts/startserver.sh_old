export PROJECT_PROFILE=dev
MYNAME=`basename "$0"`
source /home/mladmin/kelvinko/git-projects/azurebucket/venv/bin/activate
cd /home/mladmin/kelvinko/git-projects/azurebucket/azurebucket/

# worker = (2 x $num_cores) + 1
nohup python manage.py runserver 0.0.0.0:8000  2>&1 >> logs/${MYNAME}.`date +%y%m%d%H%M%S` &
