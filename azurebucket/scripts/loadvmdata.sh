if pidof -x "loadvmdata.sh" >/dev/null; then
    echo "Process already running"
    exit 1
fi

source /kelvinko/git-projects/azurebucket/venv/bin/activate
cd  /home/mladmin/kelvinko/git-projects/azurebucket/azurebucket/scripts
nohup python loadvmdata.py 2>&1 >> logs/loadvmdata.`date +%y%m%d%H%M%S`.log &
