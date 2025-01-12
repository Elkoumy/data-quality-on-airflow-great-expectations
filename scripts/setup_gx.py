import os
import great_expectations as gx

try:
    # Initialize Great Expectations context
    context = gx.data_context.FileDataContext()

    # Define datasource details
    datasource_name = "mysql_datasource"
    table_asset_name = "trips"
    MYSQL_CONNECTION_STRING = os.getenv("MYSQL_CONNECTION_STRING")

    # Check if the datasource already exists
    existing_datasources = context.list_datasources()
    datasource_exists = any(ds["name"] == datasource_name for ds in existing_datasources)

    if datasource_exists:
        print(f"Datasource '{datasource_name}' already exists. Skipping creation.")
    else:
        # Add the MySQL datasource
        context.sources.add_sql(
            name=datasource_name,
            connection_string=MYSQL_CONNECTION_STRING,
        )
        print(f"Datasource '{datasource_name}' added successfully.")

    # Check if the data asset already exists
    datasource = context.get_datasource(datasource_name)
    if table_asset_name in [asset.name for asset in datasource.assets]:
        print(f"Data asset '{table_asset_name}' already exists. Skipping creation.")
    else:
        # Add the table asset
        datasource.add_table_asset(
            name=table_asset_name,
            table_name="trips",
        )
        print(f"Data asset '{table_asset_name}' added successfully.")

    print("Great Expectations setup completed successfully!")

except Exception as e:
    print(f"An error occurred during Great Expectations setup: {e}")
