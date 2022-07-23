import pandas as pd
import funcs as f 
import plotly.express as px
import geopy.distance as geo
from itertools import permutations

# coords_1 = (52.2296756, 21.0122287)
# coords_2 = (52.406374, 16.9251681)
# print (geo.geodesic(coords_1, coords_2).km)

mvmts_pd = pd.read_csv("raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("raw-data/airport-codes.csv")

# storing cleaning externally to keep the file clean
ports_pd = f.cleanPortsData(ports_pd) 
mvmts_pd = f.cleanMovementsData(mvmts_pd)

port_types = ports_pd['type'].drop_duplicates()
distances_pd = pd.DataFrame( list(permutations(mvmts_pd["AIRPORT"], 2)) ).drop_duplicates()

port_types.to_csv("clean-data/port_types.csv")
distances_pd.to_csv("clean-data/distances_pd.csv")
mvmts_pd.to_csv('clean-data/mvmts_pd.csv')
ports_pd.to_csv('clean-data/ports_pd.csv')

# f.displayCoordsOnMap(
#     dataframe=ports_pd,
#     coords_lat="coords.lat", 
#     coords_lon="coords.lon", 
#     display_str="display_str")

