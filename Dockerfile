FROM python:3.9.23-alpine3.22

LABEL maintainer="harrison"

ENV PYTHONUNBUFFERED=1

# Copy requirements
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy application code
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .temp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .temp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /app/vol/files/static && \
    mkdir -p /app/vol/files/media && \
    chown -R django-user:django-user /app/vol/files/static && \
    chown -R django-user:django-user /app/vol/files/media && \
    chmod -R 755 /app/vol/files/static

ENV PATH="/py/bin:$PATH"

USER django-user
