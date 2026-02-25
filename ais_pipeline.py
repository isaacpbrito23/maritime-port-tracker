import requests
import pandas as pd
from datetime import datetime
import os

#My API key that was generated at myshiptracking.com, along with
#the specific port code for Suape port in Brazil.
API_KEY = "MY_API_KEY"

#I used the Suape port as an example, but you can put any
#port code and the code will have the same results.
PORT_CODE = "BRSUA"



API_URL = f"https://api.myshiptracking.com/api/v2/port/inport?unloco={PORT_CODE}"


def fetch_port_data(): #function to fetch the port data

	try: #Using a try block to not have any messy failures
		print(f"{datetime.now()} Asking MyShipTracking who is at Port {PORT_CODE}...")

                #passing API key inside of an HTTP header for security
		secure_headers = { 
			"x-api-key": API_KEY
		}

		response = requests.get(API_URL, headers=secure_headers) #safety tripwire
		response.raise_for_status() #check for errors
		data = response.json()

		
		#using '[]' in case the port is empty
		raw_ships = data.get("data", []) 
		clean_ships = []

		#looping through payload with only the data I want to extract
		for ship in raw_ships:
			vessel_info = {
				"scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"vessel_name": ship.get("name"),
				"mmsi_number": ship.get("mmsi"),
				"imo_number": ship.get("imo"),
				"vessel_type": ship.get("type"),
				"ship_flag": ship.get("flag"),
				"year_built": ship.get("built"),
				"length": ship.get("length")
			}

			clean_ships.append(vessel_info)

		return clean_ships
	#Catch any network or API connection errors and save specific
	#error message as 'e'.
	except requests.exceptions.RequestException as e:
		print(f"Error fetching data: {e}")
		return None 

#storage function (saving to a csv file)
def save_to_csv(data_list):
	
	#Quick guardrail in case the fetch fails or the port is empty
	if not data_list:
		print("No ships found or API failed.")

		return


	csv_filename = "BRSUA_port_log.csv"
	
	#Pandas maps the keys
	df = pd.DataFrame (data_list) 
	
	#If the file doesn't exist yet, it will run the next line of code
	if not os.path.isfile(csv_filename):
		#Converting from pandas default to comma separated values,
		#and turning off row numbers.
		df.to_csv(csv_filename, index=False)

	else: #appends new data instead of creating a new file and deleting
	      #the old one.

		df.to_csv(csv_filename, mode = 'a', header=False, index=False)

	#logging statement
	print(f"Saved{len(data_list)} ships to {csv_filename}")

#Check if this script is being executed directly 
if __name__ == "__main__":

	#Store the raw data list in a variable
	port_data = fetch_port_data()

	#Pass the list into a storage pipeline to safely append to CSV
	save_to_csv(port_data)

