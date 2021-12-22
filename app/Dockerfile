FROM python:3.10

WORKDIR /app
COPY --chown=1 . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--pythonpath", "/", "-w", "2", "-b", "0.0.0.0:5000", "api:app"]
