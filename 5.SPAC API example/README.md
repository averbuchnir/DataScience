# Data Fetching and Processing Script

## Overview
This script fetches environmental data from the Plant-DiTech API based on an experiment ID and processes it into a CSV file.

## Configuration
The script reads configuration settings from `config.json`, which includes:

- **AUTHORIZATION**: The API token for authentication.
- **EXPERIMENT_ID**: The ID of the experiment to fetch data from.
- **CONTROL_SYSTEM_ID**: The control system ID for the request.
- **START_DATE**: The starting date for the data request.
- **YESTERDAY**: The ending date for the data request.
- **PARAMETERS**: A list of parameters (e.g., weather conditions) to request.
- **PLANTS_ID**: A list of plant identifiers to filter the data.
- **FILES**: A list of file names to save the output data.

## How to Use
1. Ensure `config.json` is correctly set up.
2. Run the script:
   ```sh
   python main.py
