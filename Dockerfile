# Base image
FROM apache/airflow:2.4.0

# Switch to root to install system dependencies
USER root

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    libmariadb-dev \
    libssl-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch to the airflow user for Python package installation
USER airflow

# Install Python dependencies for both Airflow and Great Expectations
RUN pip install --no-cache-dir \
    pymysql \
    great-expectations==0.15.34 \
    apache-airflow-providers-mysql \
    apache-airflow-providers-http \
    airflow-provider-great-expectations

# Set working directory
WORKDIR /app

# Copy application-specific scripts and configurations
USER root
COPY ./scripts /app/scripts
#COPY gx /app/great_expectations
COPY ./requirements.txt /app/requirements.txt

# Adjust permissions for the entrypoint script
RUN chmod +x /app/scripts/gx-entrypoint.sh  \
    && chmod +x /app/scripts/airflow-entrypoint.sh

# Switch back to airflow user
USER airflow

# Install additional Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose ports for Airflow and Great Expectations
EXPOSE 8080 8081 8000

# Default entrypoint
ENTRYPOINT ["/app/scripts/gx-entrypoint.sh"]
