
import pandas as pd
import numpy as np
import funcs as f 
import plotly.express as px
import geopy.distance as geo
from itertools import permutations

# coords_1 = (52.2296756, 21.0122287)
# coords_2 = (52.406374, 16.9251681)
# print (geo.geodesic(coords_1, coords_2).km)

# ingest raw data after it gets pulled from the API in the separate file
mvmts_pd = pd.read_csv("raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("raw-data/airport-codes.csv")

# cleaning stored externally to keep main clean
ports_pd = f.cleanPortsData(ports_pd) 
mvmts_pd = f.cleanflightsData(mvmts_pd)

port_types = ports_pd["type"].drop_duplicates()
distances_pd = pd.DataFrame(list(permutations(mvmts_pd["AIRPORT"], 2))).drop_duplicates()
distances_pd.columns = ["Airport_From", "Airport_To"]

# # uncomment for scenario analysis - demonstrates how many duplicates are present in the generated dataset
# # set yearly volumes again to overide what is set by default
# sample_list = f.randomScenarioAnalysisDuplicateCheck(mvmts_pd, 50000, 0.1, 10)


# # using realistic volumes will crash your computer! It's a lot of movments :^)
# yearly_volume_raw = mvmts_pd["Dom_Acm_In"].sum() # 606,565 flights in total
yearly_volume_raw = 10000
duplicates_moe = 0.0

gen_flights_object = f.generateflightsScenario(mvmts_pd, yearly_volume_raw, duplicates_moe)
gen_flights = gen_flights_object["data"]
gen_flights_summary = gen_flights_object["summary"]

# print(gen_flights_summary.loc[gen_flights_summary["Airport"] == "SYDNEY"])
gen_flights_summary["merge string"] = gen_flights_summary["Airport"].str.lower()

temp_pd = ports_pd.drop_duplicates(subset=["municipality"]).copy()
temp_pd["merge string"] = temp_pd["municipality"].str.lower()

gen_flights_summary = pd.merge(gen_flights_summary, temp_pd[["merge string", "coords-lat", "coords-lon"]], how="left", on="merge string")
# gen_flights_summary["latlong"] = [gen_flights_summary["coords-lat"]]

# port_types.to_csv("clean-data/port_types.csv")
# distances_pd.to_csv("clean-data/distances_pd.csv")
# mvmts_pd.to_csv("clean-data/mvmts_pd.csv")
# ports_pd.to_csv("clean-data/ports_pd.csv")
# gen_flights.to_csv("clean-data/gen_flights.csv")
gen_flights_summary.to_csv("clean-data/gen_flights_summary.csv")

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat="coords.lat", 
#     coords_lon="coords.lon", 
#     display_str="display_str")

