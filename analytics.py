import pandas as pd 
import numpy as np 
import copy
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import matplotlib.colors as colors
import geopandas as gpd

from geopy.geocoders import Nominatim 
from functools import partial


# figure specs
plt.rcParams["figure.figsize"] = (12, 6)

#geolocator to map latitude and longitude to city and federal state
geolocator = Nominatim(user_agent="mapping_coordinates_to_federalstates")

#dic federal states & number of comps in that states [all, 2003-2013, 2014-$rn]
federalStaes = {
    'Schleswig-Holstein' : [0, 0, 0],
    'Mecklenburg-Vorpommern' : [0, 0, 0],
    'Hamburg' : [0, 0, 0],
    'Bremen' : [0, 0, 0],
    'Niedersachsen' : [0, 0, 0],
    'Sachsen-Anhalt' : [0, 0, 0],
    'Brandenburg' : [0, 0, 0],
    'Berlin' : [0, 0, 0],
    'Nordrhein-Westfalen' : [0, 0, 0],
    'Hessen' : [0, 0, 0],
    'Thüringen' : [0, 0, 0],
    'Sachsen' : [0, 0, 0],
    'Rheinland-Pfalz' : [0, 0, 0],
    'Saarland' : [0, 0, 0],
    'Baden-Württemberg' : [0, 0, 0],
    'Bayern' : [0, 0, 0]
}

# just a dic to think that something is more efficient because not borthering geolocator all the time
cities = {'none' : 'nothing'}

# data import
Comps = pd.read_csv('data/WCA_export_Competitions.tsv', sep='\t')


# mapping citys to federal states
def city_state(city):
    if city == 'Berlin': #city states are not haldeled correctly by geolocator
        return 'Berlin'
    elif city == 'Hamburg':
        return 'Hamburg'
    elif city == 'Lampertheim':
        #warum auch immer Lampertehim zu irgendwas im Elsass zeigt
        return 'Hessen'
    else:
        location = geolocator.geocode(city)
        coord = str(location.latitude) + ", " + str(location.longitude)
        location = geolocator.reverse(coord, exactly_one=True)
        address = location.raw['address']
        state = address.get('state', '')
        return state 


# iterate over comps and fill federalStates dic
# german comps only
dfG = Comps[Comps['countryId'] == 'Germany']
print(dfG.info())
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
            
        federalStaes[state][0] = federalStaes[state][0] + 1



# generate map
dfr = gpd.read_file("./GISPORTAL_GISOWNER01_GERMANY_STATES_15.shp")
rr = pd.DataFrame.from_dict(federalStaes, orient = 'index').reset_index(drop = False)
print(rr)
rr = rr.rename(columns = {'index':'StateName1'})
dfr = dfr.merge(rr, on = 'StateName1')
print(dfr)



karte = copy.copy(cm.hot_r)
karte = colors.LinearSegmentedColormap.from_list('green', 
                                        [(0,    '#B3FF80'),
                                         (0.5, '#299617'),
                                         (1,    '#005C29')], N=256)


#joining model outputs to the shapefile
fig, ax = plt.subplots(figsize = (15,12))
fig.subplots_adjust(top=0.95)
fig.suptitle('Distribution of WCA Competitions',fontsize = 15)
dfr.plot(column = 0,cmap = karte,ax=ax, legend=True)
dfr.geometry.boundary.plot(color=None,edgecolor='k',linewidth = 1,ax=ax) 

#adding labels
dfr['coords'] = dfr['geometry'].apply(lambda x: x.representative_point().coords[:])
dfr['coords'] = [coords[0] for coords in dfr['coords']]
print(dfr)
for idx, row in dfr.iterrows():
    plt.annotate(text=str(row[0]), xy=row['coords'], horizontalalignment='center')


plt.savefig("foo.png")
        
        


