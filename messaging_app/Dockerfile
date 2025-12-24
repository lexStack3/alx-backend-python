FROM python:3.10

RUN useradd -m -s /bin/bash app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN chown -R app:app /app

USER app

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

# Port mapping is done at runtime using: docker run -p 8080:8000 messaging_app
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
