FROM python:3.4.3

ENV FLASK_CONFIG=production
WORKDIR /www
ADD . /www
RUN pip install -r requirements.txt
RUN python manage.py db upgrade

EXPOSE 5000

CMD python run.py
