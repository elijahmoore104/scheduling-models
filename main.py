from os import error
import requests
import json
import pandas as pd

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

response = requests.get("https://data.gov.au/data/api/3/action/datastore_search?resource_id=c1a3f0db-89d0-4b84-b82a-d065ca30e7a3")
response_data = response.json()

# jprint(response.json())

# data = pd.json_normalize(
#     response_data, 
#     'success',
#     errors='ignore'
#     )

# print(data)


