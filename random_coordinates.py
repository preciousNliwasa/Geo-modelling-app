import numpy as np
import pandas as pd

def create_dataset(lat_min : float,lat_max : float,lng_min : float,lng_max : float,points:int):
    
    np.random.seed(35)
    
    point_lat = np.random.random(10000000)
    
    lat = []
    
    for i in point_lat:
        
        if (i + lat_min ) > lat_max:
            
            pass
            
        elif (i + lat_min ) < lat_min:
            
            pass
            
        elif ((i + lat_min ) >= lat_min) and ((i + lat_min ) <= lat_max):
            
            lat.append(i + lat_min)
       
    point_lat = np.random.choice(lat,size = points,replace = False)
    
    point_lng = np.random.random(10000000)
    
    lng = []
    
    for i in point_lng:
        
        if (i + lng_min ) > lng_max:
            
            pass
            
        elif (i + lng_min ) < lng_min:
            
            pass
            
        elif ((i + lng_min ) >= lng_min) and ((i + lng_min ) <= lng_max):
            
            lng.append(i + lng_min)
       
    point_lng = np.random.choice(lng,size = points,replace = False)
    
    Location = pd.DataFrame({'Lat':point_lat,'Lng':point_lng})
    
    return Location
    