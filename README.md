#🚢 Suape Maritime Port Tracker


#Overview

##This project is an ETL (Extrat, Transform, Load) pipeline that monitors live maritime traffic at the port of Suape (BRSUA) in Brazil.
##It connects to the MyShipTracking REST API to fetch real-time vessel telemetry, cleans and formats the data, 
##and logs it into a continuously growing historical CSV database. 

#The process:

1. The extract: Reaches out to MyShipTracking API API using secure header authentication to
   download a raw JSON payload of all vessels currently docked or anchored at the port.
2. The Transform: Parses the JSON array, filtering out unnecessary data while keeping only the data I want
   (Time of scan, vessel name, MMSI, IMO, vessel type, year built, length and flag). It also injects a custom `datetime` stamp and a
   hardcoded port status for accurate historical tracking.
4. The Load: Passes the cleaned dictionary to the `pandas` library, which safely appends the new data to
   `BRSUA_port_log.csv` without overwriting historical records or duplicating headers.

#Technology Stack
-Language: Python 3
-Data manipulation: pandas
-Network ops: Requests (REST APIs, JSON parsing)
-Automation: Linux `cron` (Scheduled to run automatically at the top of every hour)
-Environment: Ubuntu Linux VM

#Data Schema
The output database (`BRSUA_port_log.csv`) tracks the following columns:

1. `scan_time`: Local timestamp of the API ping (YYYY-MM-DD HH:MM:SS)
2. `status`: Current vessel state (e.g., "Currently In Port")
3. `vessel_name`: Registered name of the ship
4. `ship_flag`: Country code of the vessel's registration
5. `mmsi_number`: Maritime Mobile Service Identity
6. `imo_number`: International Maritime Organization number
7. `vessel_type`: Classification (e.g., Tug, Tanker, Cargo)
