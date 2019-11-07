cd /home/mladmin/kelvinko/git-projects/azurebucket/azurebucket/
nohup python manage.py runserver 0.0.0.0:8000  2>&1 >> logs/serverlog.`date +%y%m%d%H%M%S` &
