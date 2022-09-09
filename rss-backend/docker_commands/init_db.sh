#!/bin/bash

until python -m weedly.db create 2>init_db_logs
  do 
    echo "БД не готова, пробуем через 10 сек"
    sleep 10
  done

python -m weedly.db add-test-rss

gunicorn -w 4 -b 0.0.0.0:5000 weedly.app:app
