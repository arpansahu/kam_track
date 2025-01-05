FROM python:3.10.7

WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy the rest of the application
COPY . .

# Copy supervisord configuration file

# Expose necessary ports
EXPOSE 8018 8055

# Start supervisord to manage the processes
# CMD ["supervisord", "-c", "supervisord.conf"]

# Run all processes in the foreground
# CMD bash -c "uvicorn kam_track.asgi:application --host 0.0.0.0 --port 8018 & \
#               celery -A kam_track.celery worker -l info -n kam_track_worker & \
#               celery -A kam_track beat -l info & \
#               celery -A kam_track flower --port=8055"

CMD bash -c "uvicorn kam_track.asgi:application --host 0.0.0.0 --port 8018 & \
              celery -A kam_track.celery worker -l info -n kam_track_worker & \
              celery -A kam_track beat -l info & \
              celery -A kam_track flower --port=8055"