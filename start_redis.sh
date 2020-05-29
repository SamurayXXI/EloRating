#!/bin/bash

docker run -d -p 6379:6379 redis
celery -A EloRating worker -l info &
flower -A EloRating --port=5555 &
ps ax | grep celery