#!/bin/bash

# Wait for the MySQL service to be ready
echo "Waiting for MySQL to start..."
while ! mysqladmin ping -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" --silent; do
    sleep 2
done
echo "MySQL is ready!"

# Initialize Great Expectations if not already done
if [ ! -f "/app/gx/great_expectations.yml" ]; then
    echo "Initializing Great Expectations..."
    great_expectations --assume-yes init

fi

# Run the setup script to configure GX
if python /app/scripts/setup_gx.py; then
    echo "Great Expectations setup completed successfully."
else
    echo "Great Expectations setup encountered an error." >&2
    exit 1
fi

# Run the checkpoint script to validate data
if python /app/scripts/run_checkpoint.py; then
    echo "Checkpoint executed successfully."
else
    echo "Checkpoint execution encountered an error." >&2
    exit 1
fi

#exec "$@"
# Keep the container running indefinitely
echo "GreatExpectations Setup complete. Keeping the container running..."
tail -f /dev/null
