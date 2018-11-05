docker run -d --rm --link uekpartnership_postgres_1:pg --net uekpartnership_default postgres:10-alpine

while ! pg_isready -U postgres -h pg
do
    echo "waiting for start"
    sleep 10
done
echo "postgres is ready"
