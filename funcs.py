from random import sample
import requests
import json
import pandas as pd
import numpy as np
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
        (input_pd.type!="") & # currently blank but change if certain port types should be removed
        (input_pd.iso_country=="AU"), 
        ["iso_country","coords", "name", "type", "municipality"]].drop_duplicates()
    input_pd = input_pd.fillna("")
    input_pd["coords.lon"] = input_pd["coords"].str.extract(r'(.*),') # left of commma
    input_pd["coords.lat"] = input_pd["coords"].str.extract(r',(.*)') # right of commma
    input_pd["display_str"] = input_pd["name"] + " | " + input_pd["municipality"] + " | " + input_pd["type"]

    return input_pd

def cleanMovementsData(input_pd):
    input_pd = input_pd.loc[input_pd["AIRPORT"] != "TOTAL AUSTRALIA"] #remove totals otherwise sum is doubled
    input_pd = input_pd.copy()

    input_pd['Dom_In_Pct'] = (input_pd['Dom_Acm_In'] / input_pd.groupby('Year_Ended_December')['Dom_Acm_In'].transform('sum'))
    input_pd['Dom_Out_Pct'] = (input_pd['Dom_Acm_Out'] / input_pd.groupby('Year_Ended_December')['Dom_Acm_Out'].transform('sum'))

    # Filter to 2019 to start with. A generalized solution will come later
    input_pd = input_pd.loc[input_pd["Year_Ended_December"] == 2019]
    input_pd = input_pd.drop([
        "Rank",
        "Int_Acm_In", 
        "Int_Acm_Out", 
        "Int_Acm_Total",
        "Acm_In", 
        "Acm_Out",
        "Acm_Total"
        ], axis=1)

    input_pd['Dom_moves_per_day'] = input_pd.Dom_Acm_Total / 365
    input_pd['Rank'] = input_pd["Dom_Acm_Total"].rank(ascending = False)
    input_pd = input_pd.sort_values(by="Rank")

    return input_pd

def generateRandomSet(list_of_items, distribution, attempts):
    # test = np.array()
    out_arr = []
    for i in range(0, attempts):
        temp = np.random.choice(list_of_items, p = distribution)
        out_arr.append(temp)

    # out_arr_vals = out_arr["ports"].value_counts().reset_index()
    return out_arr

def randomScenarioAnalysisDuplicateCheck(mvmts_pd, yearly_volume, samples):
    sample_list = []
    for i in range(0,samples):
        gen_port_calls_Out = pd.DataFrame(generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Doc_Out_Pct"], yearly_volume), columns=["ports"])
        gen_port_calls_In  = pd.DataFrame(generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Doc_In_Pct"], yearly_volume), columns=["ports"])
        gen_port_calls = gen_port_calls_Out.merge(gen_port_calls_In, left_index=True, right_index=True)
        calls_amount = len(gen_port_calls)
        duplicates_val = len(gen_port_calls.drop(gen_port_calls[gen_port_calls.ports_x != gen_port_calls.ports_y].index))
        duplicates_pct = duplicates_val / calls_amount
        sample_list.append([duplicates_val, duplicates_pct*100])
        print(i, ",", round(sample_list[i][1],3), "| ", end ="")
    print()
    # print(sample_list)
    
    sample_pcts = [x[1] for x in sample_list]
    sample_duplicates = [x[0] for x in sample_list]

    print("scenarios:", samples)
    print("average duplicates val:", np.average(sample_duplicates))
    print("calls:", calls_amount)
    print("average duplicates pct:", np.average(sample_pcts))
    sample_pd = pd.DataFrame(sample_list)
    return sample_pd