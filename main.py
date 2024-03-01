
import requests
import json
import logging
from memory_profiler import profile
import os

# import os for slash symbol, it will automatically pick the type of slash 
# for the operating system (slash on linux, backslash on windows)

url = "https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt"

# Create and configure logger
logging.basicConfig(level=logging.INFO,
                    filename="CensusDataProcess.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()

# the @profile decorator is used to profile the process_census_data function. 
# the process_census_data is then executed, and the memory usage of the function is recorded. 
# Finally, the results of the profiling are printed to the console. 
@profile
def process_census_data(url):
    state_counties = {}

    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        for line in lines:
            parts = line.strip().split('|')
            state = parts[0]
            county_name = parts[4]
            
            if state not in state_counties:
                state_counties[state] = []
                
            state_counties[state].append(county_name)
    else:
        print("Failed to fetch data from the URL.")
        logger.info(f"Failed to fetch data from the URL.")

    return state_counties

 
def print_census_data(data):
    print(json.dumps(data, indent=2))
    

# Write data to JSON file
def write_data_file(data): 

    if(bool(data)):
        with open(os.path.join('json_output','output_json.json'), 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Data has been written to : {json_file}.")
        logger.info(f"File Created : {json_file}.")
    else:
        logger.info(f"No data from the source, file not created")


def lambda_handler(event, context):
    """
    Entry point for the Lambda function.
    """
    logger.info("Start processing Lambda handler!")

    try: 
        write_data_file(event)      
        return {
            'statusCode': 200,
            'body': json.dumps({'result': event})
        }        
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid input. Please provide a valid url.')
        } 

if __name__ == "__main__":
    event_data = process_census_data(url)
    # Call the lambda_handler function locally
    response = lambda_handler(event_data, None)
    logger.info(f"Ended process.")
