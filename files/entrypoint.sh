#!/bin/bash

wait-for-it -t 30 redis:6379
wait-for-it -t 30 mongodb:27017

exec "$@"