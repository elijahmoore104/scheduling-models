import decimal
import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px
from itertools import permutations
from random import randrange
import datetime as dt

from scheduling.Location import Location


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
        gen_port_calls_out = pd.DataFrame(generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Dom_out_Pct"], yearly_volume), columns=["ports"])
        gen_port_calls_in  = pd.DataFrame(generateRandomSet(mvmts_pd["AIRPORT"], mvmts_pd["Dom_in_Pct"], yearly_volume), columns=["ports"])
        gen_port_calls = gen_port_calls_out.merge(gen_port_calls_in, left_index=True, right_index=True)
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

def generateScheduleScenario(mvmts_pd, yearly_volume_raw, margin_of_error):
    yearly_volume_inflated = int(yearly_volume_raw*(1+margin_of_error))

    gen_schedule_out = pd.DataFrame(generateRandomSet(mvmts_pd["Airport"], mvmts_pd["Dom_out_Pct"], yearly_volume_inflated), columns=["ports"])
    gen_schedule_in  = pd.DataFrame(generateRandomSet(mvmts_pd["Airport"], mvmts_pd["Dom_in_Pct"], yearly_volume_inflated), columns=["ports"])
    gen_schedule_raw = gen_schedule_out.merge(gen_schedule_in, left_index=True, right_index=True)
    duplicates_val = len(gen_schedule_raw.drop(gen_schedule_raw[gen_schedule_raw.ports_x != gen_schedule_raw.ports_y].index))
    duplicates_pct = (duplicates_val / yearly_volume_inflated)*100

    # drop duplicates, to create the final schedule data
    gen_schedule = gen_schedule_raw.drop(gen_schedule_raw[gen_schedule_raw.ports_x == gen_schedule_raw.ports_y].index)
    scenario_volume = len(gen_schedule)
    
    gen_schedule.columns = ["Airport_From", "Airport_To"]
    
    # generate a random flight time for the year. Currently a manual workaround for only 2019
    gen_schedule["Flight_DateTime"] = generateScheduleTimes(yearly_volume_raw, dt.datetime(2019, 1, 1), dt.datetime(2020, 1, 1))

    # summarize ports by aggregate schedule volume in the period
    gen_schedule_out_summary = gen_schedule_out.value_counts().reset_index()
    gen_schedule_in_summary = gen_schedule_in.value_counts().reset_index()
    gen_schedule_out_summary.columns = ["Airport", "Dom_Acm_out_Simulated"]
    gen_schedule_in_summary.columns = ["Airport", "Dom_Acm_in_Simulated"]
    # gen_schedule_out_summary["Airport"] = gen_schedule_out_summary["Airport"].str.upper().str.replace(" ", "_")
    # gen_schedule_in_summary["Airport"] = gen_schedule_in_summary["Airport"].str.upper().str.replace(" ", "_")

    gen_schedule_summary = gen_schedule_out_summary.merge(gen_schedule_in_summary)
    # gen_schedule_values = gen_schedule_summary[gen_schedule_summary["index"] == "SYDNEY"]

    schedule_object = {
        "test": {"next_level": "output"},
        "data": gen_schedule,
        "summary": gen_schedule_summary
    }

    return schedule_object

def generateDistancesTable(input_col, col_names):
    output_pd = pd.DataFrame(list(permutations(input_col, 2))).drop_duplicates()
    output_pd.columns = col_names
    output_pd = output_pd.apply(lambda x: x.astype(str).str.upper().str.replace(" ", "_"))

    return output_pd

def generateScheduleTimes(volume, date_lower, date_upper):
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




def generateScheduleScenarioLocationObj(locations: list, yearly_volume_raw: int, margin_of_error: decimal):
    yearly_volume_inflated = int(yearly_volume_raw*(1+margin_of_error))


    gen_schedule_out = pd.DataFrame(generateRandomSet(mvmts_pd["Airport"], mvmts_pd["Dom_out_Pct"], yearly_volume_inflated), columns=["ports"])
    gen_schedule_in  = pd.DataFrame(generateRandomSet(mvmts_pd["Airport"], mvmts_pd["Dom_in_Pct"], yearly_volume_inflated), columns=["ports"])
    gen_schedule_raw = gen_schedule_out.merge(gen_schedule_in, left_index=True, right_index=True)
    duplicates_val = len(gen_schedule_raw.drop(gen_schedule_raw[gen_schedule_raw.ports_x != gen_schedule_raw.ports_y].index))
    duplicates_pct = (duplicates_val / yearly_volume_inflated)*100

    # drop duplicates, to create the final schedule data
    gen_schedule = gen_schedule_raw.drop(gen_schedule_raw[gen_schedule_raw.ports_x == gen_schedule_raw.ports_y].index)
    scenario_volume = len(gen_schedule)
    
    gen_schedule.columns = ["Airport_From", "Airport_To"]
    
    # generate a random flight time for the year. Currently a manual workaround for only 2019
    gen_schedule["Flight_DateTime"] = generateScheduleTimes(yearly_volume_raw, dt.datetime(2019, 1, 1), dt.datetime(2020, 1, 1))

    # summarize ports by aggregate schedule volume in the period
    gen_schedule_out_summary = gen_schedule_out.value_counts().reset_index()
    gen_schedule_in_summary = gen_schedule_in.value_counts().reset_index()
    gen_schedule_out_summary.columns = ["Airport", "Dom_Acm_out_Simulated"]
    gen_schedule_in_summary.columns = ["Airport", "Dom_Acm_in_Simulated"]
    # gen_schedule_out_summary["Airport"] = gen_schedule_out_summary["Airport"].str.upper().str.replace(" ", "_")
    # gen_schedule_in_summary["Airport"] = gen_schedule_in_summary["Airport"].str.upper().str.replace(" ", "_")

    gen_schedule_summary = gen_schedule_out_summary.merge(gen_schedule_in_summary)
    # gen_schedule_values = gen_schedule_summary[gen_schedule_summary["index"] == "SYDNEY"]

    schedule_object = {
        "test": {"next_level": "output"},
        "data": gen_schedule,
        "summary": gen_schedule_summary
    }

    return schedule_object
