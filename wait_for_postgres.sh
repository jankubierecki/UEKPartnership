until docker run --link uekpartnership_postgres_1:pg --net docker-compose_default postgres:alpine pg_isready -U postgres -h pg; do sleep 1; done

