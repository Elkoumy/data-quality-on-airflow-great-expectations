# Data Validation with Great Expectations

This repository contains scripts and configurations for validating data using the Great Expectations library. The primary script, `run_checkpoint.py`, demonstrates how to load data from a MySQL database, define expectations, and validate the data.

## Features

- **Data Loading**: Load data from a MySQL database into a Pandas DataFrame.
- **Expectation Suite**: Define and manage expectation suites to validate data.
- **Validation**: Validate data against defined expectations and generate validation results.
- **Data Docs**: Build and view data documentation for validation results.

## Getting Started

### Prerequisites

- Python 3.7+
- MySQL database
- Great Expectations library
- SQLAlchemy library
- Pandas library

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Elkoumy/data-quality-on-airflow-great-expectations.git
    cd data-quality-on-airflow-great-expectations
    ```

2. Install the required Python packages:
    ```sh
    docker-compose up --build
    ```


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
Distributed under the MIT License. See `LICENSE` for more information.
```

