
from urllib import response
import pandas as pd
import funcs as f 

"""
    Data is pulled from government website via API
        Movements data:
            Source information      https://data.gov.au/dataset/ds-dga-cc5d888f-5850-47f3-815d-08289b22f5a8/details
            API endpoint            https://data.gov.au/data/api/3/action/datastore_search?resource_id=c1a3f0db-89d0-4b84-b82a-d065ca30e7a3
            More info               --

    Data pulled from open source website - information updated daily
        Airport codes data:
            Source information      https://datahub.io/core/airport-codes
            API endpoint            https://pkgstore.datahub.io/core/airport-codes/airport-codes_json/data/9ca22195b4c64a562a0a8be8d133e700/airport-codes_json.json
            More info               https://datahub.io/core/airport-codes/datapackage.json
"""

url_mvmts = "https://data.gov.au/data/api/3/action/datastore_search?resource_id=c1a3f0db-89d0-4b84-b82a-d065ca30e7a3&limit=32000"
url_portcodes = "https://pkgstore.datahub.io/core/airport-codes/airport-codes_json/data/9ca22195b4c64a562a0a8be8d133e700/airport-codes_json.json"

movements_json = f.getJsonFromApi(url_mvmts)
portcode_json = f.getJsonFromApi(url_portcodes)

pd_movements = f.normalizeAndSaveLocal(movements_json['result']['records'], 'raw-data/airport-movement-data.csv')
pd_port_codes = f.normalizeAndSaveLocal(portcode_json, "raw-data/airport-codes.csv")


# data_pd = pd.read_csv("airport_movement_data.csv")
# print(data_pd)


print(pd_movements)

