while ! nc -z localhost 9000
do
	echo "Retrying..."
	sleep 2
done