# Dockerfile
FROM python:3.10

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd


# Install pipenv
RUN pip install pipenv

# # Ensure Pipfile.lock is removed (if it exists from prior builds)
# RUN rm -f Pipfile.lock
COPY ./wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app/

# Expose port
EXPOSE 8000
