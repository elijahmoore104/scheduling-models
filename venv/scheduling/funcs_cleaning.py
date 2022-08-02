import pandas as pd
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
    input_pd["coords_lon"] = input_pd["coords"].str.extract(r'(.*),').astype(float) # left of commma
    input_pd["coords_lat"] = input_pd["coords"].str.extract(r',(.*)').astype(float) # right of commma
    input_pd['latlong'] = input_pd[['coords_lat', 'coords_lon']].values.tolist()
    input_pd["municipality"] = input_pd["municipality"].str.upper().str.replace(" ","_")
    
    # input_pd.loc[input_pd.name == "Sunshine Coast Airport", 'municipality'] = "SUNSHinE_COAST"
    # input_pd.loc[input_pd.name == "King Island Airport", 'municipality'] = "KinG_ISLAND"
    # input_pd.loc[input_pd.name == "Palm Island Airport", 'municipality'] = "PALM_ISLAND"

    input_pd["display_str"] = input_pd["name"] + " | " + input_pd["municipality"] + " | " + input_pd["type"]

    return input_pd

def cleanScheduleData(input_pd):
    input_pd.rename(columns={'AIRPORT':'Airport'}, inplace=True)
    input_pd["Airport"] = input_pd["Airport"].str.upper().str.replace(" ", "_")
    input_pd = input_pd.loc[input_pd["Airport"] != "TOTAL_AUSTRALIA"].copy() #remove totals otherwise sum is doubled

    input_pd['Dom_in_Pct'] = (input_pd['Dom_Acm_In'] / input_pd.groupby('Year_Ended_December')['Dom_Acm_In'].transform('sum'))
    input_pd['Dom_out_Pct'] = (input_pd['Dom_Acm_Out'] / input_pd.groupby('Year_Ended_December')['Dom_Acm_Out'].transform('sum'))

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

