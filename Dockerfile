# Dockerfile
FROM python:3.10

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gnupg2 ca-certificates \
    && curl -fsSL https://ftp-master.debian.org/keys/archive-key-12.asc | tee /etc/apt/trusted.gpg.d/archive-key-12.asc \
    && curl -fsSL https://ftp-master.debian.org/keys/archive-key-13.asc | tee /etc/apt/trusted.gpg.d/archive-key-13.asc \
    && apt-get clean


RUN apt-get update && apt-get install -y netcat-openbsd


# Install pipenv
RUN pip install pipenv

##############################
# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock to install dependencies in the pipenv environment
COPY Pipfile Pipfile.lock /app/

# Install project dependencies using pipenv
RUN pipenv install --system --deploy
############################################
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
