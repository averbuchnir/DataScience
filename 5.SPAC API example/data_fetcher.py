import json
import requests
import pandas as pd
import time

def load_config(file_path="config.json"):
    """
    Loads configuration variables from a JSON file.

    Args:
        file_path (str): Path to the JSON configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Configuration file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None

def make_request(url, headers):
    """
    Sends an HTTP GET request to the given URL with the specified headers.

    Args:
        url (str): The URL to send the GET request to.
        headers (dict): A dictionary containing the headers for the request.

    Returns:
        dict: The response JSON parsed into a dictionary, or None if the request failed.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def process_and_save_data(json_data, params, plants, file_name):
    """
    Processes the JSON data returned from the API and saves it to a CSV file.

    Args:
        json_data (dict): The JSON data to process.
        params (str): The parameter key for which to extract the data.
        plants (list): A list of plant identifiers for the data.
        file_name (str): The name of the CSV file to save the data to.
    """
    try:
        arr_data = json_data["group1"]["data"][params]
        dicty = {}
        temp_ts = []

        for plant in plants:
            temp_arr = []
            for ts in arr_data:
                temp_ts.append(ts[0])
                temp_arr.extend(ts[1:])
            dicty[plant] = temp_arr

        df = pd.DataFrame(dicty)
        df["Timestamp"] = temp_ts
        df.set_index("Timestamp", inplace=True)
        df.to_csv(file_name)
        print(f"Data saved to {file_name}")
    except KeyError as e:
        print(f"Key error processing data: {e}")
    except Exception as e:
        print(f"Error during data processing: {e}")

def build_url(experiment_id, control_system_id, start_date, yesterday, plants, params):
    """
    Constructs the API request URL with the given parameters.

    Args:
        experiment_id (int): The experiment ID.
        control_system_id (int): The control system ID.
        start_date (str): Start date in YYYY-MM-DD format.
        yesterday (str): End date in YYYY-MM-DD format.
        plants (list): List of plant IDs.
        params (str): The parameter to fetch.

    Returns:
        str: The constructed URL.
    """
    return (
        f"http://spac.plant-ditech.com/api/data/getData?"
        f"experimentId={experiment_id}&"
        f"controlSystemId={control_system_id}&"
        f"fromDate={start_date}T00:00:00.000Z&"
        f"toDate={yesterday}T23:59:59.999Z&"
        f"plants={','.join(plants)}&"
        f"params={params}"
    )
