import time
from data_fetcher import load_config, make_request, process_and_save_data, build_url, get_control_systems,get_plant_table
start_time = time.time()

def main():
    """
    Main function to orchestrate the data fetching, processing, and saving.
    """
    start_time = time.time()

    # Load configuration
    config = load_config()
    if not config:
        return

    # Assign config values
    AUTHORIZATION = config["AUTHORIZATION"]
    EXPERIMENT_ID = config["EXPERIMENT_ID"]
    CONTROL_SYSTEM_ID = config["CONTROL_SYSTEM_ID"]
    START_DATE = config["START_DATE"]
    YESTERDAY = config["YESTERDAY"]
    PARAMETERS = config["PARAMETERS"]
    PLANTS_ID = config["PLANTS_ID"]
    FILES = config["FILES"]

    headers = {'Authorization': AUTHORIZATION}
    # Fetch and print control system data
    try:
        control_systems = get_control_systems(headers)
        print(f"Control systems: {control_systems}")
    except Exception as e:
        print(f"Error fetching control systems: {e}")
        pass    

    # fetch the plant table of specific control system
    try:
        plant_table_message = get_plant_table(headers, EXPERIMENT_ID, CONTROL_SYSTEM_ID)
        print(plant_table_message)
    except Exception as e:
        print(f"Error fetching plant table: {e}")
        pass

    for idx, params in enumerate(PARAMETERS):
        url = build_url(EXPERIMENT_ID, CONTROL_SYSTEM_ID, START_DATE, YESTERDAY, PLANTS_ID, params)

        print(f"Requesting data for {params}...")
        json_data = make_request(url, headers)
        # get the plant_table df 
        plant_table_df = get_plant_table(headers, EXPERIMENT_ID, CONTROL_SYSTEM_ID, return_df=True)
        # create dict based on ID and Name
        PLANTS_ID_DICT = dict(zip(plant_table_df["ID"], plant_table_df["Name"]))
  
        if json_data:
            file_name = f"{FILES[idx] if idx < len(FILES) else f'data_{params}.csv'}"
            process_and_save_data(json_data, params, PLANTS_ID, file_name,PLANTS_ID_DICT)

print(f"Process completed in {time.time() - start_time:.3f} seconds.")
if __name__ == "__main__":
    main()
