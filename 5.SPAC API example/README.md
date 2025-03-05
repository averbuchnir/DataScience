
# SPAC API Data Fetcher Project

This project is designed to facilitate the automated and interactive fetching and processing of environmental data from the Plant-DiTech API. It provides two main modes of operation: a batch mode (`main_by_config.py`) for automated processing based on predefined settings, and an interactive mode (`main_interactive.py`) for user-guided data fetching and processing.

---

## Configuration

The project relies on a configuration file named `config.json` that must be supplied by the user. This file should contain the necessary settings to authenticate and make API requests.

### `config.json` Structure:

- **AUTHORIZATION**: The API token for authentication.

For `main_interactive.py`, the only required field is:
- **AUTHORIZATION**: The API token for authentication.

For `main_by_config.py`, the following fields must be filled with valid values:
- **EXPERIMENT_ID**: Any valid integer (e.g., `14`).
- **CONTROL_SYSTEM_ID**: Any valid integer (e.g., `42`).
- **START_DATE**: Any valid date (e.g., `"2025-03-03"`).
- **YESTERDAY**: Any valid date (e.g., `"2025-03-03"`).
- **PARAMETERS**: Any valid parameters (e.g., `["s244"]`).
- **PLANTS_ID**: Any valid list of IDs (e.g., `[25550,25551,25552, ...]`).
- **FILES**: Any valid filenames (e.g., `["s244.csv"]`).

Ensure this configuration file is correct and present in the same directory as the scripts before running them.

---

## Components

### Scripts

- **data_fetcher.py**:  
  Contains utility functions to load configurations, make API requests, and process the fetched data into CSV files.

- **main_by_config.py**:  
  Operates in a non-interactive batch mode using the configuration file `config.json` to automate the entire data fetching and processing workflow.

- **main_interactive.py**:  
  Provides an interactive interface to manually select experiments, adjust dates, and fetch data, which is then processed and saved.

### Usage Instructions

#### Batch Mode (`main_by_config.py`)

**Functionality**:
- Automatically reads settings from `config.json`.
- Fetches and processes data based on predefined settings.
- Saves the processed data in CSV format in specified file names.

**Execution**:
```bash
python main_by_config.py
```

#### Interactive Mode (`main_interactive.py`)

**Functionality**:
- Prompts users to select specific experiments and settings dynamically.
- Allows for date adjustments and interactive confirmation of control system and experiment IDs.
- Fetches and processes data interactively, logging actions for review.

**Execution**:
```bash
python main_interactive.py
```
Follow the on-screen prompts to navigate through the data fetching process.

---

## Installation and Requirements

**Python Version**:
- Python 3.x

**Dependencies**:
- `requests`
- `pandas`
- `logging`

Install the required Python packages using pip:
```bash
pip install requests pandas
```

---

## Notes

- Ensure that the `config.json` file is always updated with the correct and current API credentials and settings before running the scripts.
- The `data_fetcher.py` script must not be run directly; it only serves as a support module for the other two scripts.
- All files (`config.json`, `data_fetcher.py`, `main_by_config.py`, and `main_interactive.py`) should be located in the same directory.

---

## Support

For issues, suggestions, or further assistance, please contact [averbuch.nir@gmail.com](mailto:averbuch.nir@gmail.com) or [nir.averbuch@mail.huji.ac.il](mailto:nir.averbuch@mail.huji.ac.il).

---

Happy Data Fetching!
