FROM python:3.11-slim-bullseye

WORKDIR /app

# Install curl and docker CLI
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/

CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0"]

