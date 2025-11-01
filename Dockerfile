FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y netcat-traditional libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

RUN chmod +x /code/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]

