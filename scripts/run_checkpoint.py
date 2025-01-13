import great_expectations as gx
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.core.batch import RuntimeBatchRequest
import pandas as pd
from sqlalchemy import create_engine

# Load the context
context = gx.get_context()

# Define the expectation suite
suite_name = "default_expectation_suite"
try:
    suite = context.get_expectation_suite(suite_name)
except gx.exceptions.DataContextError:
    suite = context.create_expectation_suite(suite_name)

# Load data from MySQL into a Pandas DataFrame
mysql_connection_string = "mysql+pymysql://root:password@mysql:3306/my_database"  # Replace with your actual connection string
engine = create_engine(mysql_connection_string)
query = "SELECT * FROM trips"
batch_data = pd.read_sql(query, con=engine)

# Define the RuntimeBatchRequest
batch_request = RuntimeBatchRequest(
    datasource_name="mysql_datasource",
    data_connector_name="default_runtime_data_connector_name",
    data_asset_name="trips",  # Name of the logical data asset
    runtime_parameters={"batch_data": batch_data},  # Pass the DataFrame directly
    batch_identifiers={"default_identifier_name": "batch_001"}  # A unique identifier for this batch
)

# Get a validator using the RuntimeBatchRequest and the expectation suite
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=suite_name,
)

# Add expectations
validator.expect_column_values_to_not_be_null(column="pickup_datetime")
validator.expect_column_values_to_not_be_null(column="passenger_count")
validator.expect_column_values_to_be_between(column="congestion_surcharge", min_value=0, max_value=1000)

# Save the expectation suite
validator.save_expectation_suite()

results = validator.validate()

# Save results and build data docs
context.build_data_docs()

# Print validation results
print(results)

