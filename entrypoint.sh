#!/bin/sh
set -e

# load .env if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# wait for db (simple loop)
echo "Waiting for database..."
n=0
until nc -z ${DB_HOST:-db} ${DB_PORT:-5432} || [ $n -ge 30 ]; do
  n=$((n+1))
  echo "Waiting for db... ($n)"
  sleep 1
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec "$@"
