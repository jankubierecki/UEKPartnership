until docker run --rm --link uekpartnership_postgres_1:pg --net uekpartnership_default postgres:latest pg_isready -U postgres -h pg; do sleep 1; done

