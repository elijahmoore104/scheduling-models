
from urllib import response
import pandas as pd
import funcs as f 

"""
    Data is pulled from government website via API
        https://data.gov.au/dataset/ds-dga-cc5d888f-5850-47f3-815d-08289b22f5a8/details
        
        API call (without set limit)
        https://data.gov.au/data/api/3/action/datastore_search?resource_id=c1a3f0db-89d0-4b84-b82a-d065ca30e7a3
"""

# response_data = f.getJsonFromApi("https://data.gov.au/data/api/3/action/datastore_search?resource_id=c1a3f0db-89d0-4b84-b82a-d065ca30e7a3&limit=32000")

# data_pd = pd.json_normalize(response_data['result']['records'])
# data_pd.to_csv('airport_movement_data.csv')

response_data = pd.read_csv("airport_movement_data.csv")
print(response_data)




