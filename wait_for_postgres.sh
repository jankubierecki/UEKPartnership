docker run --rm --link uekpartnership_postgres_1:pg --net uekpartnership_default postgres:10-alpine

while ! pg_isready
do
    echo "waiting for start"
    sleep 10
done
echo "postgres is ready"
