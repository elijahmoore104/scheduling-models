
from turtle import distance
import pandas as pd
import numpy as np
import funcs as f 
import plotly.express as px
import geopy.distance as geo


# ingest raw data after it gets pulled from the API in separate file
mvmts_pd = pd.read_csv("raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("raw-data/airport-codes.csv")

# cleaning stored externally to keep main tidy
ports_pd = f.cleanPortsData(ports_pd) 
mvmts_pd = f.cleanflightsData(mvmts_pd)
distances_pd = f.generateDistancesTable(mvmts_pd["AIRPORT"], ["Airport_From", "Airport_To"])
port_types = ports_pd["type"].drop_duplicates()

# # uncomment for scenario analysis - demonstrates how many duplicates are present in the generated dataset
# sample_list = f.randomScenarioAnalysisDuplicateCheck(mvmts_pd, 50000, 0.1, 10)

# # using realistic volumes will crash your computer! It's a lot of movments :^)
# yearly_volume_raw = mvmts_pd["Dom_Acm_In"].sum() # 606,565 flights in total
yearly_volume_raw = 10000
duplicates_moe = 0.0

gen_flights_object = f.generateflightsScenario(mvmts_pd, yearly_volume_raw, duplicates_moe)
gen_flights = gen_flights_object["data"]
gen_flights_summary = gen_flights_object["summary"]

# print(gen_flights_summary.loc[gen_flights_summary["Airport"] == "SYDNEY"])
gen_flights_summary["merge_string"] = gen_flights_summary["Airport"].str.upper().str.replace(" ", "_")

temp_pd = ports_pd.drop_duplicates(subset=["municipality"]).copy()
temp_pd["merge_string"] = temp_pd["municipality"]

gen_flights_summary = pd.merge(gen_flights_summary, temp_pd[["merge_string", "latlong"]], how="left", on="merge_string")
# gen_flights_summary = gen_flights_summary.drop(columns=["merge string"])

# coords_1 = [52.2296756, 21.0122287]
# coords_2 = [52.406374, 16.9251681]
coords_1 = gen_flights_summary.loc[1, "latlong"]
coords_2 = gen_flights_summary.loc[2, "latlong"]

print(coords_1, coords_2)
print (geo.geodesic(coords_1, coords_2).km)


# port_types.to_csv("clean-data/port_types.csv")
distances_pd.to_csv("clean-data/distances_pd.csv")
# mvmts_pd.to_csv("clean-data/mvmts_pd.csv")
ports_pd.to_csv("clean-data/ports_pd.csv")
# gen_flights.to_csv("clean-data/gen_flights.csv")
gen_flights_summary.to_csv("clean-data/gen_flights_summary.csv")

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat="coords.lat", 
#     coords_lon="coords.lon", 
#     display_str="display_str")

