import pandas as pd
import numpy as np
import scheduling

# test = scheduling.Plane("Soarer21", "Elijah", 2)

def cleanPortsData(input_pd):
    input_pd = pd.DataFrame(input_pd).rename(columns={"coordinates": "coords"})
    input_pd = input_pd.loc[
        (input_pd.type!="") & # currently blank but change if certain port types should be removed
        (input_pd.iso_country=="AU"), 
        ["iso_country","coords", "name", "type", "municipality"]].drop_duplicates()
    input_pd = input_pd.fillna("")
    input_pd["name_adjusted"] = input_pd["name"].str.upper().str.replace(" AIRPORT", "").str.replace(" ", "_")
    input_pd["coords_lon"] = input_pd["coords"].str.extract(r"(.*),").astype(float) # left of commma
    input_pd["coords_lat"] = input_pd["coords"].str.extract(r",(.*)").astype(float) # right of commma
    input_pd["latlong"] = input_pd[["coords_lat", "coords_lon"]].values.tolist()
    input_pd["municipality"] = input_pd["municipality"].str.upper().str.replace(" ","_")
    
    # input_pd.loc[input_pd.name == "Sunshine Coast Airport", "municipality"] = "SUNSHinE_COAST"
    # input_pd.loc[input_pd.name == "King Island Airport", "municipality"] = "KinG_ISLAND"
    # input_pd.loc[input_pd.name == "Palm Island Airport", "municipality"] = "PALM_ISLAND"

    input_pd["display_str"] = input_pd["name"] + " | " + input_pd["municipality"] + " | " + input_pd["type"]

    return input_pd

def cleanScheduleData(input_pd):
    input_pd = input_pd.iloc[:,2:]
    input_pd.rename(columns={"AIRPORT":"Airport"}, inplace=True)
    input_pd["Airport"] = input_pd["Airport"].str.upper().str.replace(" ", "_")
    input_pd = input_pd.loc[input_pd["Airport"] != "TOTAL_AUSTRALIA"].copy() #remove totals otherwise sum is doubled

    input_pd["Dom_in_Pct"] = (input_pd["Dom_Acm_In"] / input_pd.groupby("Year_Ended_December")["Dom_Acm_In"].transform("sum"))
    input_pd["Dom_out_Pct"] = (input_pd["Dom_Acm_Out"] / input_pd.groupby("Year_Ended_December")["Dom_Acm_Out"].transform("sum"))

    # Filter to 2019 to start with. A generalized solution will come later
    input_pd = input_pd.loc[input_pd["Year_Ended_December"] == 2019]
    input_pd = input_pd.drop([
        "Rank",
        "Int_Acm_In", "Int_Acm_Out", "Int_Acm_Total",
        "Acm_In", "Acm_Out", "Acm_Total"
        ], axis=1)
    
    input_pd["Dom_moves_per_day"] = input_pd.Dom_Acm_Total / 365
    input_pd["Rank"] = input_pd["Dom_Acm_Total"].rank(ascending = False)
    input_pd = input_pd.sort_values(by="Rank")

    # rename ports to match ports_pd
    # input_pd["Airport"].replace("THURSDAY_ISLAND", "HORN_ISLAND")
    # input_pd["Airport"].replace(["ESSENDON_FIELDS"], "MELBOURNE_ESSENDON")
    input_pd["Airport"] = input_pd["Airport"].replace(
        ["THURSDAY_ISLAND","ESSENDON_FIELDS", "NORFOLK_ISLAND", "EDWARD_RIVER", "MCARTHUR_RIVER"], 
        ["HORN_ISLAND", "MELBOURNE_ESSENDON", "NORFOLK", "PORMPURAAW", "MCARTHUR_RIVER_MINE"])

    input_pd.reset_index(drop=True, inplace=True)

    return input_pd

def getLatlongFromLocations(mvmts_pd, ports_pd):
    # merge ports and flights data together
    temp_pd = ports_pd.drop_duplicates(subset=["municipality"]).copy()
    temp_pd["Airport"] = temp_pd["municipality"]
    mvmts_pd_temp = pd.merge(mvmts_pd, temp_pd[["Airport", "coords_lat", "coords_lon"]], how="left", on="Airport")

    temp_pd = ports_pd.drop_duplicates(subset=["name_adjusted"]).copy()
    temp_pd["Airport"] = temp_pd["name_adjusted"]
    mvmts_pd_temp = pd.merge(mvmts_pd_temp, temp_pd[["Airport", "coords_lat", "coords_lon"]], how="left", on="Airport")

    mvmts_pd_temp["final_coords_lat"] = np.where(mvmts_pd_temp["coords_lat_x"].isnull(), mvmts_pd_temp["coords_lat_y"], mvmts_pd_temp["coords_lat_x"])
    mvmts_pd_temp["final_coords_lon"] = np.where(mvmts_pd_temp["coords_lon_x"].isnull(), mvmts_pd_temp["coords_lon_y"], mvmts_pd_temp["coords_lon_x"])
    mvmts_pd_temp = mvmts_pd_temp.drop(columns=["coords_lat_x", "coords_lat_y", "coords_lon_x", "coords_lon_y"]).rename(columns={
            "final_coords_lat": "coords_lat",
            "final_coords_lon": "coords_lon"
            })
    
    coords_list = {
        "CHRISTMAS_ISLAND": list([10.4510, 105.6889]),
        "COCOS_ISLAND": list([12.1880, 96.8293])
    }

    # assign latlongs for the leftover ports that are None after the merge    
    mvmts_pd_temp.loc[mvmts_pd_temp["Airport"] == "CHRISTMAS_ISLAND", ["coords_lat", "coords_lon"]] = [coords_list["CHRISTMAS_ISLAND"][0], coords_list["CHRISTMAS_ISLAND"][1]]
    mvmts_pd_temp.loc[mvmts_pd_temp["Airport"] == "COCOS_ISLAND", ["coords_lat", "coords_lon"]] = [coords_list["COCOS_ISLAND"][0], coords_list["COCOS_ISLAND"][1]]

    mvmts_pd_temp = mvmts_pd_temp.dropna()
    # mvmts_pd_temp = mvmts_pd_temp[mvmts_pd_temp["coords_lat"].isnull()]
    # mvmts_pd_temp = mvmts_pd_temp[mvmts_pd_temp["coords_lon"].isnull()]

    return mvmts_pd_temp

