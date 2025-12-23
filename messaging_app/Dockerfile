FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

# Port mapping is done at runtime using: docker run -p 8080:8000 messaging_app
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
