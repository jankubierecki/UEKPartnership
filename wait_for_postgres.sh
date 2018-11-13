until docker run --rm --link $(docker inspect --format='{{.Name}}' $(docker ps -aq --no-trunc) | cut -c2- | grep postgres):pg --net uekpartnership_default postgres:10-alpine pg_isready -U postgres -h pg; do sleep 2; done;
echo "postgres is fully ready"
