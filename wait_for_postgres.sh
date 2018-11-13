until docker run postgres:10-alpine pg_isready -U postgres -h pg -p 5432; do sleep 2; done;
echo "postgres is ready"