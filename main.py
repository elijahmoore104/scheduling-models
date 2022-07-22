
import pandas as pd
import funcs as f 
import plotly.express as px


mvmts_pd = pd.read_csv("raw-data/airport-movement-data.csv")
ports_pd = pd.read_csv("raw-data/airport-codes.csv")
# print(ports_pd)

# mvmts_pd = pd.DataFrame(mvmts_pd).rename(columns={"coordinates": "coords"})
ports_pd = pd.DataFrame(ports_pd).rename(columns={"coordinates": "coords"})
test = ports_pd.loc[
    (ports_pd.type!="") &
    (ports_pd.iso_country=="AU"), 
    ["iso_country","coords", "name", "type", "municipality"]].drop_duplicates()

test = test.fillna("")

test["coords.lon"] = test["coords"].str.extract(r'(.*),') # left of commma
test["coords.lat"] = test["coords"].str.extract(r',(.*)') # right of commma
test["display_str"] = test["name"] + " | " + test["municipality"] + " | " + test["municipality"]

test.to_csv('test4.csv')

f.displayCoordsOnMap(
    dataframe=test,
    coords_lat="coords.lat", 
    coords_lon="coords.lon", 
    display_str="display_str")

