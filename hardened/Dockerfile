FROM python:3.11-slim

# FIX 3: Run as non-root user
# Create a dedicated user with no shell and no home directory privileges
RUN groupadd -r appgroup && useradd -r -g appgroup -s /bin/false appuser

WORKDIR /app

# Install only what is needed — no curl, no ping for production
# ping is needed for the app functionality but curl is not
RUN apt-get update && \
    apt-get install -y --no-install-recommends iputils-ping && \
    rm -rf /var/lib/apt/lists/*

RUN pip install flask

COPY app/ .

# Give ownership to appuser
RUN chown -R appuser:appgroup /app

# FIX 3 continued: switch to non-root user before running
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
