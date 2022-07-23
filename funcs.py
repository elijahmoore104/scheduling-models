import requests
import json
import pandas as pd
import plotly.express as px


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def getJsonFromApi(url):
    # https://data.gov.au/data/api/3/action/datastore_search?resource_id=c1a3f0db-89d0-4b84-b82a-d065ca30e7a3
    response = requests.get(url)
    response_data = response.json()
    return response_data

def normalizeAndSaveLocal(array, file_name):
    data_pd = pd.json_normalize(array)
    data_pd.to_csv(file_name)
    return data_pd

def displayCoordsOnMap(dataframe: pd.DataFrame, coords_lat: str, coords_lon: str, display_str: str, color=["blue"]):
    fig = px.scatter_geo(dataframe, lat=coords_lat,lon=coords_lon, hover_name=display_str, color_discrete_sequence=color)
    # fig.update_layout(title = 'Map of Airports', title_x=0.5)
    fig.show()

def cleanPortsData(input_pd):
    input_pd = pd.DataFrame(input_pd).rename(columns={"coordinates": "coords"})
    input_pd = input_pd.loc[
        (input_pd.type!="") &
        (input_pd.iso_country=="AU"), 
        ["iso_country","coords", "name", "type", "municipality"]].drop_duplicates()
    input_pd = input_pd.fillna("")
    input_pd["coords.lon"] = input_pd["coords"].str.extract(r'(.*),') # left of commma
    input_pd["coords.lat"] = input_pd["coords"].str.extract(r',(.*)') # right of commma
    input_pd["display_str"] = input_pd["name"] + " | " + input_pd["municipality"] + " | " + input_pd["municipality"]

    return input_pd

def cleanMovementsData(input_pd):
        
    input_pd = input_pd.loc[input_pd["AIRPORT"] != "TOTAL AUSTRALIA"]
    input_pd = input_pd.copy()

    input_pd['Doc_In_Pct'] = (input_pd['Dom_Acm_In'] / input_pd.groupby('Year_Ended_December')['Dom_Acm_In'].transform('sum'))
    input_pd.loc['Doc_Out_Pct'] = input_pd['Dom_Acm_Out'] / input_pd.groupby('Year_Ended_December')['Dom_Acm_Out'].transform('sum')

    # Filter to 2019 to start with. A generalized solution will come later
    input_pd = input_pd.loc[input_pd["Year_Ended_December"] == 2019]

    return input_pd