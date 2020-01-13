export NUMOFCORES=`grep -c ^processor /proc/cpuinfo`
export NUMOFWORKERS=`expr $NUMOFCORES \* 2 + 1`

if [[ "${DJANGO_ENV}" = "DEV" ]] ; then
export DJANGO_PORT=8000
export DJANGO_DEBUG=True
elif [[ "${DJANGO_ENV}" = "PROD" ]] ;then
export DJANGO_PORT=80
export DJANGO_DEBUG=False
else
export DJANGO_PORT=8000
export DJANGO_DEBUG=True
fi

if [[ -z "${DJANGO_API_SERVER}"  ]]; then
export DJANGO_API_ENDPOINT="http://${DJANGO_API_SERVER}:${DJANGO_PORT}/vmbucket/"
else
export DJANGO_API_ENDPOINT="http://localhost:${DJANGO_PORT}/vmbucket/"
fi
