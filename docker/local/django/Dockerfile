# Set the default Python version using an ARG
ARG PYTHON_VERSION=3.11.2-bullseye

# Base image
FROM python:${PYTHON_VERSION} as python

# Intermediate build stage
FROM python as python-build-stage
# Set the build environment using an ARG
ARG BUILD_ENVIRONMENT=local

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

# Copy requirements files to the build context
COPY ./Hy_api/requirements .

# Generate wheels for the specified build environment
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt

# Final run stage
FROM python as python-run-stage
# Set the build environment using an ARG
ARG BUILD_ENVIRONMENT=local

# Set the application home directory
ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}
WORKDIR ${APP_HOME}

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy wheels from the build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Install application dependencies from wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy entrypoint script and make it executable
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Copy start script and make it executable
COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copies the 'start' script for Celery worker from the local directory to the '/start-celeryworker' path in the Docker container
COPY ./docker/local/django/celery/worker/start /start-celeryworker  
# Removes any carriage return characters (if present) from the 'start-celeryworker' script
RUN sed -i 's/\r$//g' /start-celeryworker  
# Gives executable permissions to the 'start-celeryworker' script
RUN chmod +x /start-celeryworker  

# Copies the 'start' script for Celery Flower from the local directory to the '/start-flower' path in the Docker container
COPY ./docker/local/django/celery/flower/start /start-flower 
# Removes any carriage return characters (if present) from the 'start-flower' script
RUN sed -i 's/\r$//g' /start-flower  
# Gives executable permissions to the 'start-flower' script
RUN chmod +x /start-flower  


# Copy the application code to the application home directory
COPY . ${APP_HOME}

# Set the entrypoint for the container
ENTRYPOINT [ "/entrypoint" ]
