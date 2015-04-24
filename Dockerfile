FROM python:3.4.3

WORKDIR /www
ADD . /www
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python3 taskcube.py