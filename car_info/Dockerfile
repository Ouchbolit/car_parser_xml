# Dockerfile
FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "car_info.wsgi:application", "--bind", "0.0.0.0:8000"]
