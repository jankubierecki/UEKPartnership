until docker run --rm --link uekpartnership_postgres_1:pg --net uekpartnership_default postgres:10-alpine pg_isready -U postgres -h $(docker inspect --format='{{.Name}}' $(docker ps -aq --no-trunc) | cut -c2- | grep postgres); do sleep 2; done;
echo "postgres is ready"
