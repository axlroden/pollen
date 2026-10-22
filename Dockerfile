FROM python:3.14.9-alpine3.24

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY app /app

EXPOSE 80
CMD ["python3", "main.py"]
