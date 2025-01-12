#!/bin/bash

# Wait for the MySQL service to be ready
echo "Waiting for MySQL to start..."
while ! mysqladmin ping -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" --silent; do
    sleep 2
done
echo "MySQL is ready!"


# Run the Airflow initialization if Airflow is being started

echo "Initializing Airflow database..."
airflow db init
echo "Creating Airflow admin user..."
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
echo "Airflow initialized successfully."


airflow webserver

#exec "$@"
# Keep the container running indefinitely
echo "Airflow Setup complete. Keeping the container running..."
tail -f /dev/null
