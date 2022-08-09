import decimal
import sched
import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px
from itertools import permutations
from random import randrange
import datetime as dt

from scheduling.Location import Location
from scheduling.Trip import Trip


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

def displayCoordsOnMap(dataframe: pd.DataFrame, coords_lat: str, coords_lon: str, display_str: str, color=["blue"]) -> None:
    fig = px.scatter_geo(dataframe, lat=coords_lat,lon=coords_lon, hover_name=display_str, color_discrete_sequence=color)
    # fig.update_layout(title = 'Map of Airports', title_x=0.5)
    fig.show()

def generateRandomSet(list_of_items, distribution, attempts) -> list:
    """
        Returns an array of size 'attempts' from 'list_of_items' chosen by 'distribution'
    """
    # test = np.array()
    out_arr = []
    for i in range(0, attempts):
        temp = np.random.choice(list_of_items, p = distribution)
        out_arr.append(temp)

    # out_arr_vals = out_arr["ports"].value_counts().reset_index()
    return out_arr

def generateScheduleScenario(locations_list: list[Location], volume: int) -> list[Trip]:
    
    airports_list   = [locations_list[x].name for x in locations_list]
    distr_of_trips  = [locations_list[x].distr_of_trips for x in locations_list]

    trips = generateTripsFromDistribution(airports_list, distr_of_trips, volume)
    
    # generate a random flight time for the year. Currently a manual workaround for only 2019
    trip_times = pd.DataFrame(generateScheduleTimes(volume, dt.datetime(2019, 1, 1), dt.datetime(2020, 1, 1)))
    trips["trip_start"] = trip_times.astype("datetime64[ns]")
    # sample time used right now - all trips are 4 hours lon7g
    trips["trip_end"] = trips["trip_start"] + dt.timedelta(minutes=60*4) 

    trips.sort_values(by=["trip_start"], inplace=True)
    trips.reset_index(inplace=True, drop=True)

    return trips

def generateDistancesTable(input_col, col_names) -> pd.DataFrame:
    output_pd = pd.DataFrame(list(permutations(input_col, 2))).drop_duplicates()
    output_pd.columns = col_names
    output_pd = output_pd.apply(lambda x: x.astype(str).str.upper().str.replace(" ", "_"))

    return output_pd

def generateScheduleTimes(volume, date_lower, date_upper) -> list:
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
    # dates_pd = pd.DataFrame(d3)

    return d3

def generateTripsFromDistribution(airports_list: list, distr_of_trips: list, volume: int) -> pd.DataFrame:
    trips = []
    while len(trips) < volume:
        temp_trip = [
            generateRandomSet(airports_list, [x[0] for x in distr_of_trips], 1)[0], 
            generateRandomSet(airports_list, [x[1] for x in distr_of_trips], 1)[0]
            ]
        if temp_trip[0] != temp_trip[1]:
            trips.append(temp_trip)
        # print(temp_trip)
    trips = pd.DataFrame(trips, columns={"location_from", "location_to"})
    return trips

