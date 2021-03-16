import pickle
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import mapclassify
from geopy.exc import GeocoderTimedOut 
from geopy.geocoders import Nominatim 

def findGeocode(city): 
       
    # try and catch is used to overcome 
    # the exception thrown by geolocator 
    # using geocodertimedout   
    try: 
          
        # Specify the user_agent as your 
        # app name it should not be none 
        geolocator = Nominatim(user_agent="your_app_name") 
          
        return geolocator.geocode(city) 
      
    except GeocoderTimedOut: 
          
        return findGeocode(city)


with open('summary-v1.pkl', 'rb') as f:
    data = pickle.load(f)
date = data['wr'].apply(lambda row: pd.to_datetime(row[16:-11],infer_datetime_format=True))
wr   = data['wr'].apply(lambda row: row[-9:-1])
del data['wr']
data.insert(2, "date", date, True) 
data.insert(3, "wr", wr, True)

places = []
for i,row in enumerate(data['title']):
    if(len(row.split(':'))>1):
        if(row.split(':')[0][-2:-1]) != " ":
            places.append([i,row.split(':')[0]])



#npl = spacy.load("en_core_web_sm")
#for i,row in enumerate(data['title']):
#    doc = npl(row)
#    for ent in doc.ents:
#        if (ent.label_=='GPE'):
#            places.append(ent)
print(places)
df = pd.DataFrame(places,columns=['i','places'])

new = df.groupby(["places"]).size().reset_index(name="Rep")
#a = df.value_counts()
#
#            
print(df)

longitude = [] 
latitude = [] 
for i in (new["places"]): 
      
    if findGeocode(i) != None: 
           
        loc = findGeocode(i) 
          
        # coordinates returned from  
        # function is stored into 
        # two separate list 
        latitude.append(loc.latitude) 
        longitude.append(loc.longitude) 
       
    # if coordinate for a city not 
    # found, insert "NaN" indicating  
    # missing value  
    else: 
        latitude.append(np.nan) 
        longitude.append(np.nan)

new["Longitude"] = longitude 
new["Latitude"] = latitude 
print(new)
#map_df = gpd.read_file(df)
#
#map_df.head()
#print(data['title'])
#print(data.columns)

