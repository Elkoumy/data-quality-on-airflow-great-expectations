import os
from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

# Path to the Great Expectations directory
GX_CONFIG_PATH = "/app/great_expectations"  # Ensure this matches your mounted directory path
CHECKPOINT_NAME = "my_checkpoint"  # Replace with the name of your checkpoint

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
    Airflow DAG to validate data quality using Great Expectations.
    """

    # Start task
    start_task = DummyOperator(task_id="start")

    # Data quality task using Great Expectations
    data_quality_task = GreatExpectationsOperator(
        task_id="data_quality",
        data_context_root_dir=GX_CONFIG_PATH,
        checkpoint_name=CHECKPOINT_NAME,  # Specify your checkpoint here
        fail_task_on_validation_failure=True,
    )

    end_task = DummyOperator(task_id="end")

    # Define task dependencies
    start_task >> data_quality_task >> end_task

# Instantiate the DAG
dag_great_expectations_validation = great_expectations_validation()
