import time
import pandas as pd
from data_fetcher import (
    build_url, get_control_systems, get_experiment_parameters,
    get_plant_table, load_config, make_request, process_and_save_data
)

def ask_user(question, options):
    """Ask the user a question and return their choice."""
    while True:
        print(question)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = input("Enter your choice (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Invalid choice. Please try again.")

def main():
    """
    Interactive main function to orchestrate data fetching, processing, and saving.
    """
    start_time = time.time()

    # Load configuration
    config = load_config()
    if not config:
        return

    # Assign config values
    AUTHORIZATION = config["AUTHORIZATION"]
    PARAMETERS = config["PARAMETERS"]
    PLANTS_ID = config["PLANTS_ID"]
    FILES = config["FILES"]
    
    headers = {'Authorization': AUTHORIZATION}
    
    # Ask user which operation they want to perform
    task = ask_user("What would you like to do?", [
        "Fetch data for a specific experiment",
        "Fetch data for all available experiments",
        "Exit"
    ])

    if task == "Exit":
        print("Exiting program.")
        return
    
    # Fetch control system data
    try:
        control_systems_df = get_control_systems(headers, return_df=True)
        control_systems_df_no_dupp = control_systems_df.drop_duplicates(subset=["control_system_id", "control_system_name"])
        print("Control system data retrieved.")
    except Exception as e:
        print(f"Error fetching control systems: {e}")
        return
    print(control_systems_df_no_dupp[["control_system_id", "control_system_name"]])
    
    
    try:
        control_system_id = int(input("Enter the Control System ID: "))
        control_system_name = control_systems_df.loc[control_systems_df["control_system_id"] == control_system_id, "control_system_name"].values[0]
        confirm = input(f"Did you mean '{control_system_name}'? (y/n): ")
        if confirm.lower() != "y":
            print("Please restart and enter the correct Control System ID.")
            return
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid numerical ID.")
        return
    
    if task == "Fetch data for a specific experiment":
        filtered_experiments = control_systems_df[control_systems_df["control_system_id"] == control_system_id]
        filtered_experiments = filtered_experiments.drop_duplicates(subset=["experiment_id", "experiment_name"])
        print(filtered_experiments[["experiment_id", "experiment_name"]])
        
        try:
            experiment_id = int(input("Enter the Experiment ID: "))
            experiment_name = filtered_experiments.loc[filtered_experiments["experiment_id"] == experiment_id, "experiment_name"].values[0]
            confirm = input(f"Did you mean '{experiment_name}'? (y/n): ")
            if confirm.lower() != "y":
                print("Please restart and enter the correct Experiment ID.")
                return
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid numerical ID.")
            return
        
        experiments = [(experiment_id, control_system_id)]
    else:
        experiments = list(control_systems_df[control_systems_df["control_system_id"] == control_system_id][['experiment_id', 'control_system_id']].itertuples(index=False, name=None))
    

    for experiment_id, control_system_id in experiments:
        print(f"Processing Experiment ID {experiment_id} in Control System {control_system_id}...")
        # Fetch plant data
        try:
            plant_table_df = get_plant_table(headers, experiment_id, control_system_id, return_df=True)
            PLANTS_ID = plant_table_df["ID"].tolist()
            PLANTS_ID_DICT = dict(zip(plant_table_df["ID"], plant_table_df["Name"]))
        except Exception as e:
            print(f"Error fetching plant table: {e}")
            continue

        # Fetch experiment parameters
        try:
            experiment_params_df = get_experiment_parameters(headers, experiment_id, control_system_id, return_df=True)
            PARAMETERS = experiment_params_df["Value"].tolist()
            PARAMETERS_TO_NAME = dict(zip(experiment_params_df["Value"], experiment_params_df["Name"]))
            PARAMETERS_TO_CATEGORY = dict(zip(experiment_params_df["Value"], experiment_params_df["Category"]))
            # create dict based on Value - Name
            print("Experiment parameters retrieved.")
        except Exception as e:
            print(f"Error fetching experiment parameters: {e}")
            continue

        start_time = control_systems_df[(control_systems_df.control_system_id==control_system_id) 
                                        & (control_systems_df.experiment_id==experiment_id)]["start_time"].values[0]
        start_time_modified = pd.to_datetime(start_time).strftime("%Y-%m-%d")

        end_time = control_systems_df[(control_systems_df.control_system_id==control_system_id)
                                      & (control_systems_df.experiment_id==experiment_id)]["end_time"].values[0]
        # if end_time is NaN then set it to today, else set it to the end_time
        if pd.isna(end_time):
            end_time = pd.Timestamp.now().strftime("%Y-%m-%d")
        end_time = pd.to_datetime(end_time).strftime("%Y-%m-%d") 

   
  
        # write message that state the experiment, control system, start time and end time
        print(f"Fetching data for Experiment ID {experiment_id} in Control System {control_system_id} from {start_time_modified} to {end_time}...")
        
        # Ask user if they want to modify the start and end time
        modify_time = input("Do you want to modify the start and end time? (y/n): ")
        if modify_time.lower() == 'y':
            try:
                user_start_time = input(f"Enter the start time (current: {start_time_modified}, format: YYYY-MM-DD): ")
                user_end_time = input(f"Enter the end time (current: {end_time}, format: YYYY-MM-DD): ")
            
                # Validate the date format
                pd.to_datetime(user_start_time, format="%Y-%m-%d")
                pd.to_datetime(user_end_time, format="%Y-%m-%d")
                
                start_time_modified = user_start_time
                end_time = user_end_time
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                return

        for idx, params in enumerate(PARAMETERS):
            print(f"Requesting data for {PARAMETERS_TO_NAME[params]}...")
            url = build_url(experiment_id, control_system_id, start_time_modified, end_time, PLANTS_ID, params)
            json_data = make_request(url, headers)
            # timeout for 1 second
            time.sleep(1.5)

            if json_data:
                file_name = f"{FILES[idx] if idx < len(FILES) else f'{PARAMETERS_TO_NAME[params]}.csv'}"
                process_and_save_data(
                    json_data=json_data, 
                    params_list=params, 
                    plants=PLANTS_ID, 
                    file_name=file_name, 
                    PLANTS_ID_DICT=PLANTS_ID_DICT, 
                    headers=headers, 
                    experiment_id=experiment_id, 
                    control_system_id=control_system_id,
                    category=PARAMETERS_TO_CATEGORY[params]
                )
    

if __name__ == "__main__":
    main()
