until docker run --rm --link uekpartnership_postgres_1:pg --net docker-compose_default postgres:alpine pg_isready -U postgres -h pg; do sleep 1; done

until docker run --rm --link [CONTAINER]:pg --net [NETWORK] postgres:9.5 pg_isready -U postgres -h pg; do sleep 1; done
