export NUMOFCORES=`grep -c ^processor /proc/cpuinfo`
export NUMOFWORKERS=`expr $NUMOFCORES \* 2 + 1`

if [ $DJANGO_ENV = "DEV" ]
then
export DJANGO_PORT=8000
export DJANGO_DEBUG=True
elif [ $DJANGO_ENV = "PROD" ] 
then
export DJANGO_PORT=80
export DJANGO_DEBUG=False
else
export DJANGO_PORT=8000
export DJANGO_DEBUG=True
fi

export DJANGO_API_ENDPOINT="http://localhost:${DJANGO_PORT}/vmbucket/"
