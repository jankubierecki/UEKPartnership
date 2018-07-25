while ! nc -z 127.0.0.1 9000
do
	echo "Retrying..."
	sleep 2
done