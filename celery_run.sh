#!/usr/bin/env bash

# launch celery worker
nohup celery -A pinhead worker -l info 2>&1 > celery_worker.log &

# flower --- celery web, visit it on http://XXXX:5555/
nohup celery -A pinhead flower --address=0.0.0.0 2>&1 > celery_flower.log &