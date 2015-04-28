FROM python:3.4.3

WORKDIR /www
ADD . /www
RUN pip install -r requirements.txt

ENV FLASK_CONFIG=production

EXPOSE 5000

CMD python run.py
