until docker run --rm --link uekpartnership_postgres_1:pg --net uekpartnership_default postgres:10-alpine pg_isready -U postgres -h localhost -p 5432; do sleep 2; done;
echo "postgres is ready"