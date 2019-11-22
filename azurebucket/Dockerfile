  
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt update && apt install vim -y
RUN pip install virtualenv 
RUN virtualenv venv 
COPY requirements.txt /code/
RUN /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"
RUN /bin/bash -c "source venv/bin/activate && python manage.py migrate"
#RUN pip install -r requirements.txt
COPY . /code/
ENV  DJANGO_ENV DEV
ENV  DJANGO_DEBUG True
ENV  DJANGO_SECRET_KEY "WQWRWTWTRWE"
ENV  DJANGO_PROJECT_ROOT /code/
ENV AZURE_TENANT_ID=${AZURE_TENANT_ID}
ENV AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
ENV AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
COPY scripts/vmbucket-cron /etc/cron.d/vmbucket-cron
RUN chmod 0644 /etc/cron.d/vmbucket-cron 
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/vmbucket-cron 

#ENV  DJANGO_API_ENDPOINT="http://10.235.17.55:8000/vmbucket/"

CMD [ "./scripts/startgunicorn.sh" ]
EXPOSE 80 443 8000