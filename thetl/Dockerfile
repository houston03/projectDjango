FROM python:3.13-alpine

RUN apk add --no-cache postgresql-dev gcc musl-dev

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN mkdir -p /app/thetl/staticfiles

RUN python manage.py collectstatic --noinput

ENV PYTHONPATH="/app"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# docker-compose down --volumes
# docker-compose up -d --build


# docker exec -it de42a36d4890 sh
# python manage.py migrate
