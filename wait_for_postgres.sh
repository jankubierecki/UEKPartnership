docker run -d --rm --link uekpartnership_postgres_1:pg --net uekpartnership_default 
docker run -d postgres:alpine
until pg_isready -U postgres -h pg; do sleep 1; done
echo "postgres is ready"

