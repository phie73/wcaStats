import pandas as pd 
import numpy as np 
import copy
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import matplotlib.colors as colors
import geopandas as gpd

from geopy.geocoders import Nominatim 
from functools import partial
from datetime import datetime
from time import sleep

# figure specs
plt.rcParams["figure.figsize"] = (12, 6)

#geolocator to map latitude and longitude to city and federal state
geolocator = Nominatim(user_agent="mapping_coordinates_to_federalstates")

#dic federal states & number of comps in that states
federalStaes = {
    'Schleswig-Holstein' : 0,
    'Mecklenburg-Vorpommern' : 0,
    'Hamburg' : 0,
    'Bremen' : 0,
    'Niedersachsen' : 0,
    'Sachsen-Anhalt' : 0,
    'Brandenburg' : 0,
    'Berlin' : 0,
    'Nordrhein-Westfalen' : 0,
    'Hessen' : 0,
    'Thüringen' : 0,
    'Sachsen' : 0,
    'Rheinland-Pfalz' : 0,
    'Saarland' : 0,
    'Baden-Württemberg' : 0,
    'Bayern' : 0
}

federalStaesE = copy.copy(federalStaes)
federalStaesRN = copy.copy(federalStaes)
federalStatesY = copy.copy(federalStaes)

# just a dic to think that something is more efficient because not borthering geolocator all the time
cities = {'none' : 'nothing'}

# data import
Comps = pd.read_csv('data/WCA_export_Competitions.tsv', sep='\t')

# for one year stats
YEAR = 2023


# mapping citys to federal states
def city_state(city):
    if city == 'Berlin': #city states are not haldeled correctly by geolocator
        return 'Berlin'
    elif city == 'Hamburg':
        return 'Hamburg'
    elif city == 'Lampertheim':
        #warum auch immer Lampertehim zu irgendwas im Elsass zeigt
        return 'Hessen'
    elif city == 'Cologne':
        # klasse DB mal deutsche mal englische stadtnamen, Cologne liegt wohl in Occitanie
        return "Nordrhein-Westfalen"
    else:
        location = geolocator.geocode(city)
        sleep(1)
        coord = str(location.latitude) + ", " + str(location.longitude)
        location = geolocator.reverse(coord, exactly_one=True)
        sleep(1)
        address = location.raw['address']
        state = address.get('state', '')
        return state 


# iterate over comps and fill federalStates dic
# german comps only
dfG = Comps[Comps['countryId'] == 'Germany']
geocode = partial(geolocator.geocode, language="de")

for index, row in dfG.iterrows():
    if row['cancelled'] == True: #exclude cancelled comps cause i think they should not count
        continue
    else:      
        city = row['cityName']
        if city not in cities:
            city = city.split('-', 1)[0] #cause geolocator cannot handle citys with -
            state = city_state(city)
            cities[city] = state
        else:
            state = cities[city]
        federalStaes[state] = federalStaes[state] + 1
        if row['year'] > 2014:#comps after 2014 (2015-$rn)
            federalStaesRN[state] = federalStaesRN[state] + 1
        elif row['year'] <= 2014:
            federalStaesE[state] = federalStaesE[state] + 1
        
        if row['year'] == YEAR:
            federalStatesY[state] = federalStatesY[state] + 1



def data_to_map(dfr, compDis, nr):
    #generate map
    rr = pd.DataFrame.from_dict(compDis, orient = 'index').reset_index(drop = False)
    rr = rr.rename(columns = {'index':'StateName1'})
    dfr = dfr.merge(rr, on = 'StateName1')
    rr = rr[0:0]
    return dfr


def plot_stuff(title, legend, dfr, plt, ax, idx):
    #joining model outputs to the shapefile
    karte = copy.copy(cm.hot_r)
    karte = colors.LinearSegmentedColormap.from_list('green', 
                                        [(0,    '#B3FF80'),
                                         (0.5, '#299617'),
                                         (1,    '#005C29')], N=256)
    fig.subplots_adjust(top=0.95)
    fig.suptitle('Distribution of WCA Competitions ' + datetime.today().strftime('%Y-%m-%d'),fontsize = 15)
    dfr.plot(column = 0,cmap = karte,ax=ax[idx], legend=False)
    dfr.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 0.1,ax=ax[idx]) 
    ax[idx].set_title(title)
    ax[idx].axis('off')

    # iter over data and apply lables
    for i, row in dfr.iterrows():
        ax[idx].annotate(text=str(row[0]), xy=row['coords'], horizontalalignment='center')



fig, ax = plt.subplots(ncols=4)
dfr = gpd.read_file("./shapeFiles/GISPORTAL_GISOWNER01_GERMANY_STATES_15.shp")
#adding coords to data structure
dfr['coords'] = dfr['geometry'].apply(lambda x: x.representative_point().coords[:])
dfr['coords'] = [coords[0] for coords in dfr['coords']]


plot_stuff('2003 to 2023', False, data_to_map(dfr, federalStaes, 0), plt, ax, 0)
plot_stuff('2003 to 2014', False, data_to_map(dfr, federalStaesE, 1), plt, ax, 1)
plot_stuff('2015 to 2023', True, data_to_map(dfr, federalStaesRN, 1), plt, ax, 2)
plot_stuff('2023', False, data_to_map(dfr, federalStatesY, 1), plt, ax, 3)
plt.savefig("foo.png")

        


