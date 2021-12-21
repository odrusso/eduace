FROM python:3.10

WORKDIR /app
COPY --chown=1 . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]
