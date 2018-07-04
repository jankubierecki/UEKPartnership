#!/usr/bin/env bash
while [ "`docker-compose ps -q ${1} | wc -l`" -lt 1 ]; do
   echo "Waiting for ${1}"
  sleep 0.1;
done;

echo "Container ${1} is ready"