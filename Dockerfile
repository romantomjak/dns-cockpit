FROM python:3.7-alpine

WORKDIR /usr/src/app

RUN apk update && apk add gcc musl-dev python3-dev postgresql-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dnscockpit dnscockpit/
COPY migrations migrations/
COPY static static/
COPY alembic.ini .
COPY setup.py .

RUN pip install -e .

CMD ["python3", "dnscockpit/main.py"]
