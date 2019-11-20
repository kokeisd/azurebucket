FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENV  DJANGO_ENV DEV
ENV  DJANGO_DEBUG True
ENV  DJANGO_SECRET_KEY "WQWRWTWTRWE"
ENV  DJANGO_PROJECT_ROOT /code/
ENV  DJANGO_API_ENDPOINT="http://10.235.17.55:8000/vmbucket/"

CMD ["./scripts/startgunicorn.sh"]
EXPOSE 80 443 8000