#!/usr/bin/env bash
if [ "`docker-compose ps -q ${1}`" -eq "" ]; then
    echo "PRAWDA"
else
    echo "NIE PRAWDA"

fi

#while [ "`docker-compose ps -q ${1}`"=="" ]; do
#   echo "Waiting for ${1}"
#  sleep 0.1;
#done;

echo "Container ${1} is ready"