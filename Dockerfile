FROM python:3.8

RUN adduser testapi

WORKDIR /home/testapi

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY requirements.txt requirements.txt
COPY testapi.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP testapi.py

RUN chown -R testapi:testapi ./
USER testapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]