FROM python:3.10

RUN apt-get update && apt-get install -y default-mysql-client netcat-openbsd

RUN useradd -m -s /bin/bash app

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN chown -R app:app /app

USER app
# Port mapping is done at runtime using: docker run -p 8080:8000 messaging_app
EXPOSE 8000
