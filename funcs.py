import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px
from itertools import permutations
from random import randrange
import datetime as dt


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
    input_pd["name_adjusted"] = input_pd["name"].str.upper().str.replace(" AIRPORT", "").str.replace(" ", "_")
    input_pd["coords_lon"] = input_pd["coords"].str.extract(r'(.*),').astype(float) # left of commma
    input_pd["coords_lat"] = input_pd["coords"].str.extract(r',(.*)').astype(float) # right of commma
    input_pd['latlong'] = input_pd[['coords_lat', 'coords_lon']].values.tolist()
    input_pd["municipality"] = input_pd["municipality"].str.upper().str.replace(" ","_")
    
    # input_pd.loc[input_pd.name == "Sunshine Coast Airport", 'municipality'] = "SUNSHINE_COAST"
    # input_pd.loc[input_pd.name == "King Island Airport", 'municipality'] = "KING_ISLAND"
    # input_pd.loc[input_pd.name == "Palm Island Airport", 'municipality'] = "PALM_ISLAND"

    input_pd["display_str"] = input_pd["name"] + " | " + input_pd["municipality"] + " | " + input_pd["type"]

    return input_pd

def cleanFlightsData(input_pd):
    input_pd.rename(columns={'AIRPORT':'Airport'}, inplace=True)
    input_pd["Airport"] = input_pd["Airport"].str.upper().str.replace(" ", "_")
    input_pd = input_pd.loc[input_pd["Airport"] != "TOTAL_AUSTRALIA"].copy() #remove totals otherwise sum is doubled

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

def randomScenarioAnalysisDuplicateCheck(mvmts_pd, yearly_volume_raw, margin_of_error, samples):
    sample_list = []
    yearly_volume = int(yearly_volume_raw*(1+margin_of_error))
    for i in range(0,samples):
        gen_port_calls_Out = pd.DataFrame(generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Dom_Out_Pct"], yearly_volume), columns=["ports"])
        gen_port_calls_In  = pd.DataFrame(generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Dom_In_Pct"], yearly_volume), columns=["ports"])
        gen_port_calls = gen_port_calls_Out.merge(gen_port_calls_In, left_index=True, right_index=True)
        duplicates_val = len(gen_port_calls.drop(gen_port_calls[gen_port_calls.ports_x != gen_port_calls.ports_y].index))
        duplicates_pct = duplicates_val / yearly_volume
        sample_list.append([duplicates_val, duplicates_pct*100])
        print(i, ",", round(sample_list[i][1],3), "| ", end ="")
    print()
    print(sample_list)
    
    
    sample_duplicates = [x[0] for x in sample_list]
    sample_pcts = [x[1] for x in sample_list]
    
    sample_duplicates_average = np.average(sample_duplicates)    
    scenario_volume = yearly_volume - sample_duplicates_average 

    print("scenarios           :", samples)
    print("original port calls :", yearly_volume_raw)
    print("inflated port calls :", yearly_volume)
    print("average duplicates #:", np.average(sample_duplicates))
    print("average duplicates %:", np.average(sample_pcts))
    print("inflated accuracy   :", round(scenario_volume / yearly_volume, 5)*100)
    print("actual accuracy     :", round( scenario_volume / yearly_volume_raw, 5)*100)
    sample_pd = pd.DataFrame(sample_list)
    return sample_pd

def generateFlightsScenario(mvmts_pd, yearly_volume_raw, margin_of_error):
    yearly_volume_inflated = int(yearly_volume_raw*(1+margin_of_error))

    gen_flights_Out = pd.DataFrame(generateRandomSet(mvmts_pd["Airport"], mvmts_pd["Dom_Out_Pct"], yearly_volume_inflated), columns=["ports"])
    gen_flights_In  = pd.DataFrame(generateRandomSet(mvmts_pd["Airport"], mvmts_pd["Dom_In_Pct"], yearly_volume_inflated), columns=["ports"])
    gen_flights_raw = gen_flights_Out.merge(gen_flights_In, left_index=True, right_index=True)
    duplicates_val = len(gen_flights_raw.drop(gen_flights_raw[gen_flights_raw.ports_x != gen_flights_raw.ports_y].index))
    duplicates_pct = (duplicates_val / yearly_volume_inflated)*100

    # drop duplicates, to create the final flights data
    gen_flights = gen_flights_raw.drop(gen_flights_raw[gen_flights_raw.ports_x == gen_flights_raw.ports_y].index)
    scenario_volume = len(gen_flights)
    
    gen_flights.columns = ["Airport_From", "Airport_To"]
    
    # generate a random flight time for the year. Currently a manual workaround for only 2019
    gen_flights["Flight_DateTime"] = generateFlightTimes(yearly_volume_raw, dt.datetime(2019, 1, 1), dt.datetime(2020, 1, 1))

    # summarize ports by aggregate flights volume in the period
    gen_flights_out_summary = gen_flights_Out.value_counts().reset_index()
    gen_flights_in_summary = gen_flights_In.value_counts().reset_index()
    gen_flights_out_summary.columns = ["Airport", "Dom_Acm_Out_Simulated"]
    gen_flights_in_summary.columns = ["Airport", "Dom_Acm_In_Simulated"]
    # gen_flights_out_summary["Airport"] = gen_flights_out_summary["Airport"].str.upper().str.replace(" ", "_")
    # gen_flights_in_summary["Airport"] = gen_flights_in_summary["Airport"].str.upper().str.replace(" ", "_")


    gen_flights_summary = gen_flights_out_summary.merge(gen_flights_in_summary)
    # gen_flights_values = gen_flights_summary[gen_flights_summary["index"] == "SYDNEY"]

    flights_object = {
        "test": {"next_level": "output"},
        "data": gen_flights,
        "summary": gen_flights_summary
    }

    return flights_object

def generateDistancesTable(input_col, col_names):
    output_pd = pd.DataFrame(list(permutations(input_col, 2))).drop_duplicates()
    output_pd.columns = col_names
    output_pd = output_pd.apply(lambda x: x.astype(str).str.upper().str.replace(" ", "_"))

    return output_pd

def generateFlightTimes(volume, date_lower, date_upper):
    # d1 = dt.datetime(2019, 1, 1)
    # d2 = dt.datetime(2020, 1, 1)

    d1 = date_lower
    d2 = date_upper
    datediff = (d2-d1).days

    d3 = []
    date_size = volume
    # 24 * 2 = 48 different lots of 30m in the day to choose from. 30 minutes * {0,48} gives a random 30m interval during the day
    for i in range(0,date_size):
        random_days = randrange(0, datediff)
        random_minutes = randrange(0, 48)
        temp_date = d1 + dt.timedelta(days=random_days)
        temp_date = temp_date + dt.timedelta(minutes = 30*random_minutes)
        d3.append(temp_date)
    dates_pd = pd.DataFrame(d3)

    return dates_pd