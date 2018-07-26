until docker run --rm --link uekpartnership_postgres_1:pg postgres:alpine pg_isready -U postgres -h pg; do sleep 1; done

