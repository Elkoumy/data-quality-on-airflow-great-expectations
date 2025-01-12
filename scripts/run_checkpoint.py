import great_expectations as gx

# Load the context
context = gx.get_context()

# Define the checkpoint configuration
checkpoint = gx.checkpoint.SimpleCheckpoint(
    name="trips_validation_checkpoint",
    data_context=context,
    validations=[
        {
            "batch_request": {
                "datasource_name": "mysql_datasource",
                "data_asset_name": "trips",
            },
            "expectation_suite_name": "default_expectation_suite",
        }
    ],
)

# Run the checkpoint
result = checkpoint.run()
print(result)
