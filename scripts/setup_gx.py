import os
import yaml
import great_expectations as gx
from great_expectations.data_context import FileDataContext
from great_expectations.data_context.types.base import DataContextConfig

try:
    # Define the root directory for the Great Expectations context
    context_root_dir = "/app/great_expectations"  # Update to your actual path

    # Check if the Great Expectations configuration exists
    if not os.path.exists(f"{context_root_dir}/great_expectations.yml"):
        print("Great Expectations configuration not found. Please initialize it using `great_expectations init`.")
        exit(1)

    # Load the existing configuration
    with open(f"{context_root_dir}/great_expectations.yml", "r") as file:
        config_dict = yaml.safe_load(file)
    project_config = DataContextConfig.from_commented_map(config_dict)

    # Initialize the Great Expectations context
    context = FileDataContext(
        project_config=project_config,
        context_root_dir=context_root_dir
    )

    # Define datasource details
    datasource_name = "mysql_datasource"
    mysql_connection_string = os.getenv("MYSQL_CONNECTION_STRING")

    if not mysql_connection_string:
        raise ValueError("MYSQL_CONNECTION_STRING environment variable is not set.")

    # Check if the datasource already exists
    if datasource_name in context.datasources:
        print(f"Datasource '{datasource_name}' already exists. Skipping creation.")
    else:
        # Add the Pandas datasource
        config_dict["datasources"][datasource_name] = {
            "class_name": "Datasource",
            "execution_engine": {
                "class_name": "PandasExecutionEngine"
            },
            "data_connectors": {
                "default_runtime_data_connector_name": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["default_identifier_name"]
                }
            }
        }
        # Save the updated configuration back to the file
        with open(f"{context_root_dir}/great_expectations.yml", "w") as file:
            yaml.safe_dump(config_dict, file)
        print(f"Pandas Datasource '{datasource_name}' added successfully.")

    print("Great Expectations setup completed successfully!")

except Exception as e:
    print(f"An error occurred during Great Expectations setup: {e}")