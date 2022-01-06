FROM python:3.10

WORKDIR /app
COPY --chown=1 . /app

RUN pip install -r requirements.txt

ARG GIT_HASH_VERSION
ENV GIT_HASH_VERSION=${GIT_HASH_VERSION}

ENTRYPOINT ["gunicorn", "--pythonpath", "/", "-w", "2", "-b", "0.0.0.0:80", "api:app"]
