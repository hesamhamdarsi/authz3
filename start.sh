#!/bin/bash

echo "Running Application test..."
for _ in {1..10}; do
    flask app test > /dev/null
    rc=$?
    if [ $rc -eq 0 ]; then
        break
    fi
    sleep 10
done

if [ $rc -ne 0 ]; then
    echo "Application test failed"
    exit 1
fi

echo "Creating Database..."
flask db upgrade 

echo "Starting Application..."
if [ -z "$AUTHZ_DEBUG"]; then
    gunicorn -b 0.0.0.0:$APP_PORT \
    -w $APP_WORKERS \
    --threads $APP_THREADS \
    --access-logfile - \
    --error-logfile - \
    --log-level - \
    "authz:create_app()"
else
    gunicorn -b 0.0.0.0:$APP_PORT \
    -w $APP_WORKERS \
    --threads $APP_THREADS \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    "authz:create_app()"
fi