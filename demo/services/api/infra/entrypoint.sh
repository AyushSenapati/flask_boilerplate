#!/bin/sh

# Wait till postgres is ready to accept connections
echo Waiting for postgres...
while true; do
  flask db upgrade 2>migration.err
  exit_status=$?
  if [ $exit_status -eq 0 ]; then
    break
  fi
  echo DB init failed, retrying in 5 secs...
  sleep 5
done
echo postgres service discovered. starting server...

echo seeding data...
python manage.py seed

exec gunicorn --log-config ../infra/gunicorn_logging.conf -c ../infra/gunicorn_config.py manage:app --reload
