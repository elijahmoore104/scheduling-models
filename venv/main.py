import pandas as pd
import numpy as np
from scheduling import funcs as f
from scheduling import funcs_cleaning  as cleaning
# import plotly.express as px
# import geopy.distance as geo
# import datetime as dt

# ingest raw data after it gets pulled from the API in separate file
mvmts_pd = pd.read_csv("data/raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("data/raw-data/airport-codes.csv")

# cleaning stored externally to keep main tidy
ports_pd = cleaning.cleanPortsData(ports_pd) 
mvmts_pd = cleaning.cleanScheduleData(mvmts_pd)
distances_pd = f.generateDistancesTable(mvmts_pd["Airport"], ["Airport_From", "Airport_To"])
port_types = ports_pd["type"].drop_duplicates()

# # uncomment for scenario analysis - demonstrates how many duplicates are present in the generated dataset
# sample_list = f.randomScenarioAnalysisDuplicateCheck(mvmts_pd, 50000, 0.1, 10)

# # using realistic volumes will crash your computer! It's a lot of movments :^)
# yearly_volume_raw = mvmts_pd["Dom_Acm_In"].sum() # 606,565 flights in total
yearly_volume_raw = 5000
duplicates_moe = 0.0

gen_flights_object = f.generateScheduleScenario(mvmts_pd, yearly_volume_raw, duplicates_moe)
gen_flights = gen_flights_object["data"]
gen_flights_summary = gen_flights_object["summary"]

# merge ports and flights data together
temp_pd = ports_pd.drop_duplicates(subset=["municipality"]).copy()
temp_pd["Airport"] = temp_pd["municipality"]
gen_flights_summary = pd.merge(gen_flights_summary, temp_pd[["Airport", "latlong"]], how="left", on="Airport")

temp_pd = ports_pd.drop_duplicates(subset=["name_adjusted"]).copy()
temp_pd["Airport"] = temp_pd["name_adjusted"]
gen_flights_summary = pd.merge(gen_flights_summary, temp_pd[["Airport", "latlong"]], how="left", on="Airport")

gen_flights_summary['final_latlong'] = np.where(gen_flights_summary['latlong_x'].isnull(), gen_flights_summary['latlong_y'], gen_flights_summary['latlong_x'])
gen_flights_summary = gen_flights_summary.drop(columns=["latlong_x", "latlong_y"]).rename(columns={"final_latlong": "latlong"})
# gen_flights_summary = gen_flights_summary.dropna()
# gen_flights_summary = gen_flights_summary[gen_flights_summary["latlong"].isnull()]

# coords_1 = [52.2296756, 21.0122287]
# coords_2 = [52.406374, 16.9251681]
# coords_1 = gen_flights_summary.loc[1, "latlong"]
# coords_2 = gen_flights_summary.loc[2, "latlong"]

# print(coords_1, coords_2)
# print (geo.geodesic(coords_1, coords_2).km)

temp_pd.to_csv("data/clean-data/temp_pd.csv")
port_types.to_csv("data/clean-data/port_types.csv")
distances_pd.to_csv("data/clean-data/distances_pd.csv")
mvmts_pd.to_csv("data/clean-data/mvmts_pd.csv")
ports_pd.to_csv("data/clean-data/ports_pd.csv")
gen_flights.to_csv("data/clean-data/gen_flights.csv")
gen_flights_summary.to_csv("data/clean-data/gen_flights_summary.csv")

# print(gen_flights_summary["latlong"])

# lat = [x[0] for x in gen_flights_summary.loc[:, "latlong"]]
# lon = [x[1] for x in gen_flights_summary.loc[:, "latlong"]]

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat= lat,
#     coords_lon= lon,
#     display_str= gen_flights_summary["Airport"] )


