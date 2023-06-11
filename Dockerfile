FROM python:3.8.3-slim

# Environment variables for flask app
ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "backend.app:create_app"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

# Copying the content in the app directory. Ignoring the content in .dockerignore
COPY . /app

# Changing Working directory
WORKDIR /app 


# Installing dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt && \
    apt-get update && apt-get install -y libgomp1 gcc

# Exposing ports
EXPOSE 8000 

# Entry level command to execute
CMD gunicorn -w 4 -b 0.0.0.0 "backend.app:create_app"