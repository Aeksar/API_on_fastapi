#!/bin/bash
set -e

until pg_isready -h db -p 5432 -U postgres; do
  echo "Wait db pupupu"
  sleep 2
done

echo "start migrations"
alembic upgrade head

echo "Start app"
uvicorn main:app --host 0.0.0.0 --port 8001
