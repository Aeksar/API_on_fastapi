FROM python:3.13

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /project

COPY entrypoint.sh /app/

COPY . .

EXPOSE 8001

CMD []