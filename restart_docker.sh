#!/usr/bin/env bash
cd /root/UEKPartnership/
docker-compose pull django
docker-compose stop django nginx
docker-compose rm -f django nginx
docker volume rm uekpartnerships_static
docker volume rm uekpartnerships_nginx_config
docker-compose -p uekpartnership up -d

