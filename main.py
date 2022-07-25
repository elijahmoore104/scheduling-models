import pandas as pd
import numpy as np
import funcs as f 
import plotly.express as px
import geopy.distance as geo
from itertools import permutations

# coords_1 = (52.2296756, 21.0122287)
# coords_2 = (52.406374, 16.9251681)
# print (geo.geodesic(coords_1, coords_2).km)

mvmts_pd = pd.read_csv("raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("raw-data/airport-codes.csv")

# cleaning stored externally to keep main clean
ports_pd = f.cleanPortsData(ports_pd) 
mvmts_pd = f.cleanMovementsData(mvmts_pd)

port_types = ports_pd["type"].drop_duplicates()
distances_pd = pd.DataFrame( list(permutations(mvmts_pd["AIRPORT"], 2)) ).drop_duplicates()

yearly_volume = mvmts_pd["Dom_Acm_In"].sum()

gen_port_calls_Out = pd.DataFrame(f.generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Doc_Out_Pct"], yearly_volume), columns=["ports"])
gen_port_calls_In  = pd.DataFrame(f.generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Doc_In_Pct"], yearly_volume), columns=["ports"])

gen_port_calls = gen_port_calls_Out.merge(gen_port_calls_In, left_index=True, right_index=True)

print("port calls:", yearly_volume)

# gen_port_calls_Out_vals = gen_port_calls_Out.value_counts().reset_index()
# gen_port_calls_In_vals = gen_port_calls_In.value_counts().reset_index()
# gen_port_calls_Out_vals.columns = ["AIPORT", "Dom_Acm_Out_Simulated"]
# gen_port_calls_In_vals.columns = ["AIPORT", "Dom_Acm_In_Simulated"]
# gen_port_calls_vals = gen_port_calls_Out_vals.merge(gen_port_calls_In_vals)

# gen_port_calls_values = gen_port_calls_values[gen_port_calls_values["index"] == "SYDNEY"]
# print(gen_port_calls_values)

# port_types.to_csv("clean-data/port_types.csv")
# distances_pd.to_csv("clean-data/distances_pd.csv")
# mvmts_pd.to_csv("clean-data/mvmts_pd.csv")
# ports_pd.to_csv("clean-data/ports_pd.csv")

# gen_port_calls_Out.to_csv("clean-data/gen_port_calls_Out.csv")
# gen_port_calls_In.to_csv("clean-data/gen_port_calls_In.csv")
# gen_port_calls.to_csv("clean-data/gen_port_calls.csv")

# gen_port_calls_Out_vals.to_csv("clean-data/gen_port_calls_Out_vals.csv")
# gen_port_calls_In_vals.to_csv("clean-data/gen_port_calls_In_vals.csv")
# gen_port_calls_vals.to_csv("clean-data/gen_port_calls_vals.csv")

# gen_port_calls_values.to_csv("clean-data/gen_port_calls_values.csv")

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat="coords.lat", 
#     coords_lon="coords.lon", 
#     display_str="display_str")

