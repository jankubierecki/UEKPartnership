while ! nc -z localhost 5432
do
	echo "Retrying..."
	sleep 2
done