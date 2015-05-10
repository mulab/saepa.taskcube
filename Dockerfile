FROM python:3.4.3

ENV FLASK_CONFIG=production
WORKDIR /www
COPY requirements.txt /www/
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python run.py
