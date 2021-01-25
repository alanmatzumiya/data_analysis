
import pandas as pd
from IPython.core.display import Image
import requests

with open ("../data/google_api_key.txt", "r") as f:
    google_api_key=f.read()
    
STATIONS = pd.read_pickle('../data/HYDAT_STATIONS')
LEVELS = pd.read_pickle('../data/HYDAT_LEVELS')
FLOWS = pd.read_pickle('../data/HYDAT_FLOWS')


def mapStations(stationList, zoom=8):
    """Return a google static map showing the location of flow and level stations.
    
    Globals:
        STATIONS: Pandas dataframe with HYDAT station data.
    
    Args:
        stationList (str): List of station codes.
        zoom (int): zoom level of the resulting map.
        
    Returns:
        Image object containing the static map. Stations are displayed as:
            red: flow station
            green: level station
            yellow: flow and level
        
    """
    locs = ["{0},{1}".format(STATIONS.loc[s,'LATITUDE'], STATIONS.loc[s,'LONGITUDE']) \
             for s in stationList]
    flows = [s for s in stationList if STATIONS.loc[s,'Flow'] == True]
    levels = [s for s in stationList if STATIONS.loc[s,'Level'] == True]
    bSet = set(levels).intersection(set(flows)) 
    google_maps_url = \
        "https://maps.googleapis.com/maps/api/staticmap?" + \
        f"key={google_api_key}" + \
        "&size=640x400" + \
        f"&zoom={zoom}" + \
        "&maptype=terrain" + \
        "&markers=color:red%7Csize:mid%7Clabel:F%7C" + "|".join(["{0},{1}".format(
            STATIONS.loc[s,'LATITUDE'], STATIONS.loc[s,'LONGITUDE']) for s in set(flows).difference(bSet)]) + \
        "&markers=color:green%7Csize:mid%7Clabel:L%7C" +"|".join(["{0},{1}".format(
            STATIONS.loc[s,'LATITUDE'], STATIONS.loc[s,'LONGITUDE']) for s in set(levels).difference(bSet)]) + \
        "&markers=color:yellow%7Csize:mid%7Clabel:B%7C" + "|".join(["{0},{1}".format(
            STATIONS.loc[s,'LATITUDE'], STATIONS.loc[s,'LONGITUDE']) for s in bSet])
    return Image(requests.get(google_maps_url).content)

display(mapStations(STATIONS.index))
