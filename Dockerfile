FROM python:3.11.4-alpine

WORKDIR /opt/weathergoat

# Copy application files
ADD main.py /opt/weathergoat
ADD config.toml /opt/weathergoat
ADD requirements.txt /opt/weathergoat
COPY /bin /opt/weathergoat/bin
COPY /src /opt/weathergoat/src

# Recommended environment variables for the Python interpreter running in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IN_DOCKER 1
ENV DEBUG 0

# Precompile application files to bytecode, also deletes source .py files
RUN python bin/precompile.py

# Install required packages
RUN pip --no-cache-dir --disable-pip-version-check install -r requirements.txt

# Clean up
RUN set -x && rm -rf bin/
RUN set -x && rm requirements.txt

CMD ["python", "main.pyc"]
