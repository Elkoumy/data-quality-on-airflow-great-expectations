-- Create the database
CREATE DATABASE IF NOT EXISTS my_database;

-- Use the database
USE my_database;

-- Create the `trips` table
CREATE TABLE IF NOT EXISTS trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    pickup_datetime DATETIME NOT NULL,
    dropoff_datetime DATETIME NOT NULL,
    passenger_count INT NOT NULL,
    trip_distance FLOAT NOT NULL,
    rate_code_id INT,
    store_and_fwd_flag CHAR(1),
    pickup_location_id INT,
    dropoff_location_id INT,
    payment_type INT,
    fare_amount DECIMAL(10,2),
    extra DECIMAL(10,2),
    mta_tax DECIMAL(10,2),
    tip_amount DECIMAL(10,2),
    tolls_amount DECIMAL(10,2),
    improvement_surcharge DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    congestion_surcharge DECIMAL(10,2)
);

-- Insert some sample data
INSERT INTO trips (
    vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_distance,
    rate_code_id, store_and_fwd_flag, pickup_location_id, dropoff_location_id,
    payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount,
    improvement_surcharge, total_amount, congestion_surcharge
)
VALUES
(1, '2025-01-12 08:00:00', '2025-01-12 08:20:00', 2, 3.5, 1, 'N', 100, 200, 1, 12.00, 0.50, 0.50, 1.50, 0.00, 0.30, 14.80, 0.00),
(2, '2025-01-12 09:00:00', '2025-01-12 09:15:00', 1, 1.2, 1, 'Y', 150, 250, 2, 8.00, 0.50, 0.50, 0.00, 0.00, 0.30, 9.30, 0.00);
