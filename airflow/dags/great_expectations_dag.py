from datetime import datetime
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

# Path to the Great Expectations directory
GX_CONFIG_PATH = "/app/great_expectations"  # Update as needed
MYSQL_CONNECTION_STRING = "mysql+pymysql://root:password@mysql:3306/my_database"  # Replace with actual credentials

def validate_data_and_generate_docs():
    """
    Function to validate data using Great Expectations and generate Data Docs with statistics.
    """
    import great_expectations as gx
    from great_expectations.core.batch import RuntimeBatchRequest
    from sqlalchemy import create_engine
    import pandas as pd

    # Load Great Expectations context
    context = gx.get_context(context_root_dir=GX_CONFIG_PATH)

    # Define the expectation suite
    suite_name = "default_expectation_suite"
    try:
        suite = context.get_expectation_suite(suite_name)
    except gx.exceptions.DataContextError:
        suite = context.create_expectation_suite(suite_name)

    # Load data from MySQL into a Pandas DataFrame
    engine = create_engine(MYSQL_CONNECTION_STRING)
    query = "SELECT * FROM trips"
    batch_data = pd.read_sql(query, con=engine)

    # Define the RuntimeBatchRequest
    batch_request = RuntimeBatchRequest(
        datasource_name="mysql_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="trips",  # Logical name of the data asset
        runtime_parameters={"batch_data": batch_data},  # Pass the DataFrame directly
        batch_identifiers={"default_identifier_name": "batch_001"}
    )

    # Get a validator
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

    # Validate data
    results = validator.validate()

    # Save and build data docs
    context.build_data_docs()

    # Get Data Docs URL
    data_docs_url = context.get_docs_sites_urls()[0]["site_url"]
    print(f"Data Docs generated at: {data_docs_url}")

    # Log validation results
    if not results["success"]:
        raise ValueError(f"Data validation failed! See Data Docs for details: {data_docs_url}")
    print("Validation successful!")



@dag(
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": 300,
    },
    tags=["great_expectations_validation"],
)
def great_expectations_validation():
    """
    Airflow DAG to validate data using a Great Expectations Validator and generate Data Docs.
    """

    start_task = DummyOperator(task_id="start")

    validate_data_task = PythonOperator(
        task_id="validate_data_and_generate_docs",
        python_callable=validate_data_and_generate_docs,
    )

    end_task = DummyOperator(task_id="end")

    start_task >> validate_data_task >> end_task

# Instantiate the DAG
dag_great_expectations_validation = great_expectations_validation()
