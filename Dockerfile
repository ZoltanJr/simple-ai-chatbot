FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --default-timeout=100

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
