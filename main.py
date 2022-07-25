from pickletools import genops
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

# using realistic volumes will crash your computer! It's a lot of movments :^)
# yearly_volume_raw = mvmts_pd["Dom_Acm_In"].sum() # 606,565 port calls in total
yearly_volume_raw = 100000
duplicates_moe = 0.1
yearly_volume_inflated = int(yearly_volume_raw*(1+duplicates_moe)) #artificially inflate the yearly_volumes, since 10% are duplicates based on current match method 

# # uncomment for scenario analysis - demonstrates how many duplicates are present in the generated dataset
# # set yearly volumes again to overide what is set by default
# scenarios = 15
# yearly_volume = 10000
# duplicates_moe = 0.095
# yearly_volume = int(yearly_volume*(1+duplicates_moe))
# sample_list = f.randomScenarioAnalysisDuplicateCheck(mvmts_pd, yearly_volume, scenarios)

# gen_port_calls_Out = pd.DataFrame(f.generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Doc_Out_Pct"], yearly_volume_inflated), columns=["ports"])
# gen_port_calls_In  = pd.DataFrame(f.generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Doc_In_Pct"], yearly_volume_inflated), columns=["ports"])
# gen_port_calls_raw = gen_port_calls_Out.merge(gen_port_calls_In, left_index=True, right_index=True)
# duplicates_val = len(gen_port_calls_raw.drop(gen_port_calls_raw[gen_port_calls_raw.ports_x != gen_port_calls_raw.ports_y].index))
# duplicates_pct = (duplicates_val / yearly_volume_inflated)*100
# gen_port_calls = gen_port_calls_raw.drop(gen_port_calls_raw[gen_port_calls_raw.ports_x == gen_port_calls_raw.ports_y].index)

# scenario_volume = len(gen_port_calls)

# print("original port calls:", yearly_volume_raw)
# print("inflated port calls:", yearly_volume_inflated)
# print("inflated duplicates:", duplicates_val)
# print("port calls after rm duplicates:", scenario_volume)
# print("inflated duplicate pct:", round(1-scenario_volume / yearly_volume_inflated, 5)*100)
# print("inflated accuracy:  ", round(scenario_volume / yearly_volume_inflated, 5)*100)
# print("actual accuracy:    ", round(scenario_volume / yearly_volume_raw, 5)*100)


# gen_port_calls_Out_vals = gen_port_calls_Out.value_counts().reset_index()
# gen_port_calls_In_vals = gen_port_calls_In.value_counts().reset_index()
# gen_port_calls_Out_vals.columns = ["AIPORT", "Dom_Acm_Out_Simulated"]
# gen_port_calls_In_vals.columns = ["AIPORT", "Dom_Acm_In_Simulated"]
# gen_port_calls_vals = gen_port_calls_Out_vals.merge(gen_port_calls_In_vals)

# gen_port_calls_values = gen_port_calls_values[gen_port_calls_values["index"] == "SYDNEY"]

# port_types.to_csv("clean-data/port_types.csv")
# distances_pd.to_csv("clean-data/distances_pd.csv")
mvmts_pd.to_csv("clean-data/mvmts_pd.csv")
# ports_pd.to_csv("clean-data/ports_pd.csv")

# gen_port_calls_Out.to_csv("clean-data/gen_port_calls_Out.csv")
# gen_port_calls_In.to_csv("clean-data/gen_port_calls_In.csv")
# gen_port_calls.to_csv("clean-data/gen_port_calls.csv")
# gen_port_calls_Out_vals.to_csv("clean-data/gen_port_calls_Out_vals.csv")
# gen_port_calls_In_vals.to_csv("clean-data/gen_port_calls_In_vals.csv")
# gen_port_calls_vals.to_csv("clean-data/gen_port_calls_vals.csv")
# gen_port_calls_values.to_csv("clean-data/gen_port_calls_values.csv")
# gen_port_calls.to_csv("clean-data/gen_port_calls.csv")

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat="coords.lat", 
#     coords_lon="coords.lon", 
#     display_str="display_str")

