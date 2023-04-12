FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --no-deps -r requirements.txt --default-timeout=100

COPY . .

EXPOSE 5000

RUN python3 -m unittest discover

CMD ["flask", "run"]
