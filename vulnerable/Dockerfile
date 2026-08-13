FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y iputils-ping curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install flask

COPY app.py .
COPY templates/ templates/

EXPOSE 5000

CMD ["python", "app.py"]
