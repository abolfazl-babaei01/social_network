FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY .. .


RUN python manage.py collectstatic --noinput


CMD ["gunicorn", "-b", "0.0.0.0:8000", "social_network.wsgi:application"]