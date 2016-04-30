FROM python:3.5.1-onbuild

ENV FLASK_CONFIG=production

EXPOSE 80

CMD python run.py
