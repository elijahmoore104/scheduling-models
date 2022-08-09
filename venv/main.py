import pandas as pd
import numpy as np
from scheduling import funcs as f
from scheduling import funcs_cleaning  as cleaning
import plotly.express as px
import geopy.distance as geo
import datetime as dt
from scheduling.Location import Location

# from scheduling.Asset import Asset
# from scheduling.Trip import Trip

# test = Asset.Asset(name="eli 747", owner="eli airways")
# trip1 = Trip.Trip(test, dt.datetime(2022,1,10,12), dt.datetime(2022,1,10,12,30), "loc_from", "loc_to")

# print(test.name)
# print(trip1)


"""
    1. Create locations
    2. Pass locations object with distribution and try to create a flight (if 'location to' is 'location from' -> try again)
    3. Allocate random start time for the flight
    4. Append all flight locations w/ flight id as an object to a schedule
    5. Index the distances table to populate time stamps for the flight (taxi, take off, flight, landing, taxi
"""

# ingest raw data after it gets pulled from the API in separate file
mvmts_pd = pd.read_csv("data/raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("data/raw-data/airport-codes.csv")

# cleaning stored externally to keep main tidy
port_types = ports_pd["type"].drop_duplicates()
ports_pd = cleaning.cleanPortsData(ports_pd) 
mvmts_pd = cleaning.cleanScheduleData(mvmts_pd)
mvmts_pd = cleaning.mergePortsAndScheduleLatLong(mvmts_pd, ports_pd)
distances_pd = f.generateDistancesTable(mvmts_pd["Airport"], ["Airport_From", "Airport_To"])

locations = {}

for i in range(len(mvmts_pd)):
    airport     =    mvmts_pd.loc[i, "Airport"]
    coords_lat  =    mvmts_pd.loc[i, "coords_lat"]
    coords_lon  =    mvmts_pd.loc[i, "coords_lon"]
    distr_in    =    mvmts_pd.loc[i, "Dom_in_Pct"]
    distr_out   =    mvmts_pd.loc[i, "Dom_out_Pct"]

    locations[airport] = Location(airport, (coords_lat, coords_lon), (distr_in, distr_out))

# # using realistic volumes will crash your computer! It's a lot of movements :^)
# flight_count = mvmts_pd["Dom_Acm_In"].sum() # 606,565 flights in total
flight_count = 5

gen_flights = f.generateScheduleScenario(locations_list = locations, volume = flight_count)

print(gen_flights)

print(cleaning.getDistanceFromLatlong(locations["SYDNEY"].latlong, locations["BRISBANE"].latlong))

port_types.to_csv("data/clean-data/port_types.csv")
distances_pd.to_csv("data/clean-data/distances_pd.csv")
mvmts_pd.to_csv("data/clean-data/mvmts_pd.csv")
ports_pd.to_csv("data/clean-data/ports_pd.csv")
gen_flights.to_csv("data/clean-data/gen_flights.csv")
# gen_flights_summary.to_csv("data/clean-data/gen_flights_summary.csv")

# f.displayCoordsOnMap(
#     dataframe   = ports_pd,
#     coords_lat  = [locations[x].latlong[0] for x in locations],
#     coords_lon  = [locations[x].latlong[1] for x in locations],
#     display_str = [locations[x].name for x in locations])

