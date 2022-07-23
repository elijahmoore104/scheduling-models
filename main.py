
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
# print(ports_pd)

# mvmts_pd = pd.DataFrame(mvmts_pd).rename(columns={"coordinates": "coords"})
ports_pd = pd.DataFrame(ports_pd).rename(columns={"coordinates": "coords"})
ports_pd = ports_pd.loc[
    (ports_pd.type!="") &
    (ports_pd.iso_country=="AU"), 
    ["iso_country","coords", "name", "type", "municipality"]].drop_duplicates()

ports_pd = ports_pd.fillna("")

ports_pd["coords.lon"] = ports_pd["coords"].str.extract(r'(.*),') # left of commma
ports_pd["coords.lat"] = ports_pd["coords"].str.extract(r',(.*)') # right of commma
ports_pd["display_str"] = ports_pd["name"] + " | " + ports_pd["municipality"] + " | " + ports_pd["municipality"]

mvmts_pd = mvmts_pd[mvmts_pd["AIRPORT"] != "TOTAL AUSTRALIA"]

mvmts_pd['Doc_In_Pct'] = mvmts_pd['Dom_Acm_In'] / mvmts_pd.groupby('Year_Ended_December')['Dom_Acm_In'].transform('sum')
mvmts_pd['Doc_Out_Pct'] = mvmts_pd['Dom_Acm_Out'] / mvmts_pd.groupby('Year_Ended_December')['Dom_Acm_Out'].transform('sum')

# Filter to 2019 to start with. A generalized solution will come later
mvmts_pd = mvmts_pd[mvmts_pd["Year_Ended_December"] == 2019]

distances_pd = pd.DataFrame( list(permutations(mvmts_pd["AIRPORT"], 2)) )

distances_pd.to_csv("checks2.csv")
mvmts_pd.to_csv('mvmts_pd.csv')
ports_pd.to_csv('ports_pd.csv')

f.displayCoordsOnMap(
    dataframe=ports_pd,
    coords_lat="coords.lat", 
    coords_lon="coords.lon", 
    display_str="display_str")

