FROM python:3.13-alpine

RUN apk add --no-cache postgresql-dev gcc musl-dev

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PYTHONPATH="/app"
ENV DJANGO_SETTINGS_MODULE=djangoProject.settings


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoProject.wsgi:application"]


# docker-compose down --volumes
# docker-compose up -d --build


# docker exec -it e0642b93d58a sh
# python manage.py migrate