import json
import requests
import pandas as pd
import time
import os

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

import pandas as pd
import os

def process_and_save_data(json_data, params, plants, file_name,PLANTS_ID_DICT):
    """
    Processes the JSON data returned from the API and saves it to a CSV file in the 'pulled_data' folder.

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
        # use PLANTS_ID_DICT to replace the ID in column name with Name
        df.columns = [PLANTS_ID_DICT.get(int(col), col) for col in df.columns]


        # Ensure the directory exists
        if not os.path.exists('pulled_data'):
            os.makedirs('pulled_data')

        file_path = os.path.join('pulled_data', file_name)
        df.to_csv(file_path)
        print(f"Data saved to {file_path}")
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


def get_control_systems(headers,return_df=False):
    """
    Fetches control system data from the API, processes it, and saves it as a CSV file.

    Args:
        headers (dict): A dictionary containing the headers for the request, including Authorization.

    Returns:
        str: Path to the saved CSV file or an error message.
    """
    url = "https://api.spac.plant-ditech.com/api/controlsystem"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()
        
        # Flatten the JSON data into a table
        flattened_data = []
        for entry in data:
            for experiment in entry['experiments']:
                flattened_data.append({
                    'control_system_id': entry['id'],
                    'control_system_name': entry['name'],
                    'experiment_id': experiment['iD'],
                    'experiment_name': experiment['name'],
                    'state': experiment['state'],
                    'start_time': experiment.get('startTime', None),
                    'end_time': experiment.get('endTime', None),
                    'zero_hour': experiment['zeroHour'],
                    'daily_weight_start': experiment['dailyWeightStart'],
                    'daily_weight_duration': experiment['dailyWeightDuration'],
                    'active': experiment['active'],
                    'admin_name': experiment.get('adminName', None),
                    'admin_email': experiment.get('adminEmail', None),
                    'watering_frequency': experiment['wateringFrequency']
                })

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(flattened_data)

        # Ensure the directory exists
        directory = "control_system"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the DataFrame
        file_path = os.path.join(directory, "control_system_data.csv")
        df.to_csv(file_path, index=False)
        if return_df:
            return df
        
        return f"Data saved to {file_path}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    except Exception as e:
        return f"Error processing data: {e}"
    


def get_plant_table(headers, experiment_id, control_system_id,return_df=False):
    """
    Fetches plant and label data from the API for specified experiment and control system, processes it, and saves it as a CSV file.

    Args:
        headers (dict): A dictionary containing the headers for the request, including Authorization.
        experiment_id (int): The experiment ID to fetch data for.
        control_system_id (int): The control system ID to fetch data for.

    Returns:
        str: Path to the saved CSV file or an error message.
    """
    url = f"https://api.spac.plant-ditech.com/api/plantsandlabels?experimentId={experiment_id}&controlSystemId={control_system_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()
        
        # Flatten the JSON data into a table
        plants = []
        for plant in data['plants']:
            plants.append({
                'ID': plant['iD'],
                'Name': plant['name'],
                'Active': plant['active']
            })

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(plants)

        # Ensure the directory exists
        directory = "get_plant_table"
        if not os.path.exists(directory):
            os.makedirs(directory)

        control_systems_df = get_control_systems(headers,return_df=True)
        # get the control system name and experiment name
        control_system_name = control_systems_df[control_systems_df.control_system_id == control_system_id]["control_system_name"].values[0]
        experiment_id_name = control_systems_df[(control_systems_df.control_system_id==42) & (control_systems_df.experiment_id==3)]["experiment_name"].values[0]      
        # Save the DataFrame
        file_path = os.path.join(directory, f"{control_system_name}_{experiment_id_name}_get_plant_table.csv")
        df.to_csv(file_path, index=False)
        if return_df:
            return df
        
        return f"Data saved to {file_path}"

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

    except Exception as e:
        return f"Error processing data: {e}"
