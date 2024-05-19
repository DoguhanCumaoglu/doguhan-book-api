FROM python:3.10.5-slim

RUN apt-get update && apt-get install --no-install-recommends -y git gcc libldap2-dev libsasl2-dev libssl-dev build-essential automake autoconf && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get install --no-install-recommends -y tzdata

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]