until docker run postgres:10-alpine pg_isready -U postgres -h pg; do sleep 1; done
