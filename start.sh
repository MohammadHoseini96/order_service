#!/bin/bash

if [[ "$ENTRYPOINT" = "django" ]]
then
    echo "Apply migrations"
    python manage.py migrate
    echo "Starting web"
    gunicorn --config gunicorn_config.py  order_service.wsgi:application
elif [[ "$ENTRYPOINT" = "celery" ]]
then
    echo "Starting celery all workers"
    celery -A order_service worker -l info --pool gevent \
    --concurrency 40 --max-tasks-per-child 1000 --prefetch-multiplier 4
else
  echo Error, cannot find entrypoint "$ENTRYPOINT" to start
fi
