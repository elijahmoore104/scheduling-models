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

# # uncomment for scenario analysis - demonstrates how many duplicates are present in the generated dataset
# # set yearly volumes again to overide what is set by default
# sample_list = f.randomScenarioAnalysisDuplicateCheck(mvmts_pd, 50000, 0.1, 10)


# using realistic volumes will crash your computer! It's a lot of movments :^)
# yearly_volume_raw = mvmts_pd["Dom_Acm_In"].sum() # 606,565 port calls in total
yearly_volume_raw = 10000
duplicates_moe = 0.1
# yearly_volume_inflated = int(yearly_volume_raw*(1+duplicates_moe)) #artificially inflate the yearly_volumes, since 10% are duplicates based on current match method 

gen_movements_object = f.generateMovementsScenario(mvmts_pd, yearly_volume_raw, duplicates_moe)
gen_movements = gen_movements_object["data"]
gen_movements_summary = gen_movements_object["summary"]

port_types.to_csv("clean-data/port_types.csv")
distances_pd.to_csv("clean-data/distances_pd.csv")
mvmts_pd.to_csv("clean-data/mvmts_pd.csv")
ports_pd.to_csv("clean-data/ports_pd.csv")

# # exporting tables - doesn't really need to be done, more just for sense checks of the data when needed
# gen_movements_Out.to_csv("clean-data/gen_movements_Out.csv")
# gen_movements_In.to_csv("clean-data/gen_movements_In.csv")
# gen_movements_out_summary.to_csv("clean-data/gen_movements_out_summary.csv")
# gen_movements_in_summary.to_csv("clean-data/gen_movements_in_summary.csv")

gen_movements.to_csv("clean-data/gen_movements.csv")
gen_movements_summary.to_csv("clean-data/gen_movements_summary.csv")

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat="coords.lat", 
#     coords_lon="coords.lon", 
#     display_str="display_str")

