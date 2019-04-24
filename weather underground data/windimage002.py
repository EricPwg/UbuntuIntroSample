import matplotlib.pyplot as plt
plt.rcdefaults()
import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

import json

import urllib.request

def changme(data):
   
    wind_degrees = []
    latitude = []
    longitude = []
    wind_kph = []
    temp=[]
    for i in range(0, len(data)):
        print(data[i], i)
        response = urllib.request.urlopen('http://api.wunderground.com/api/62a57e36bca5687a/conditions/q/pws:'+data[i]+'.json')
        html = response.read()
        
        robert = json.loads(html)
        
        
        robert["response"]
        
        
        robert["current_observation"]
        
        
        wind_degrees.append( robert['current_observation']["wind_degrees"] )
        if wind_degrees == -9999:
            wind_degrees = 0
            
        wind_kph.append( robert['current_observation']["wind_kph"] )
        
        longitude.append( robert['current_observation']["observation_location"]["longitude"])
       
        temp.append(robert['current_observation']['temp_c'])
        latitude.append( robert['current_observation']["observation_location"]["latitude"])
        
        
        
    return wind_degrees, wind_kph, longitude, latitude , temp






img = mpimg.imread('Taiwan.png')
img.shape


def label(x,y, text):
    plt.text(x, y, text, ha="center", family='sans-serif', size=14)


fig, ax = plt.subplots()

patches = []

PWSf = open('PWS_list.txt', 'r')
PWSf = PWSf.readlines()

data=[]
for i in range(len(PWSf)):
    g = PWSf[i].split()
    data.append(g[0])

#data = ['I1365', 'ITAIWANK2', 'ITAIPEI19', 'I1236', 'ITAIPEI11', 'INEWTAIP4', 'I1666', 'ITAIPEI19', 'I1236', 'I1236', 'IU53F0U73','ISANXIAD4','ITPQCHAN3']
#data = ['ITAIWANK2','ISHILIND10','IU53F0U73','INEWTAIP4','I1419','IU6843U52','IHSZQING2','ITAIWAN11','IMIAOLI4','I1246','I5318','I1267','I1482','IU53F0U78','I5286','IHUALIEN3','I5291','ITAIWAND2','ICHANGHU5','ITPQDANS2']

a, q,b, p, temp= changme(data)


# add an arrow 1
#a=[90,84, 360, 355, 181, 270, 46, 89, 355, 181, 181, 145, -9999, -9999] 
#p=['25.010434','25.238205', '25.147631', '25.093197', '25.030033', '24.995480', '25.010857', '25.020317', '25.093197', '25.030033', '25.030033', '24.999760', '24.945930', '25.077608'] 
#b=['122.004208','121.613029', '121.773163', '121.558441', '121.535851', '121.537491', '121.454353', '121.415756', '121.558441', '121.535851', '121.535851', '121.507874', '121.378426', '121.376495']

log_max = 122.004208
log_min = 120.858769
lat_max = 25.010434
lat_min = 21.899509

fig_x_max = 604.713
fig_x_min = 426.621
fig_y_max = 108.613
fig_y_min = 596.483


for i in range(len(data)):
	print(p[i],b[i])
	p[i]=(float(p[i])-lat_min)/(lat_max-lat_min)*(fig_y_max-fig_y_min)+fig_y_min
	b[i]=(float(b[i])-log_min)/(log_max-log_min)*(fig_x_max-fig_x_min)+fig_x_min
	#p[i]=426.621+57.2473*(float(p[i])-21.899509)
	#b[i]=596.483-426.924*(float(b[i])-120.858769)
	print(p[i],b[i])
	q[i]=q[i]+1
	q[i]=math.log(q[i])*15
	
	dx1=-q[i]*math.cos((a[i]-90)*math.pi/180)
	dy1=-q[i]*math.sin((a[i]-90)*math.pi/180)
	print(dx1, dy1)
	arrow = mpatches.Arrow(b[i],p[i], dx1, dy1, width=math.pow(q[i],1))
	patches.append(arrow)
	label(b[i],p[i], temp[i])
	#label(b[i],p[i], data[i])



# add an arrow 2
#x2=500
#y2=300
#dx2=wd_kph[1]*math.cos(273/180*math.pi)
#dy2=wd_kph[1]*math.sin(273/180*math.pi)
#arrow = mpatches.Arrow(x2,y2, dx2, dy2, width=math.pow(wd_kph[1],1/2))
#patches.append(arrow)
#label(x2,y2, "Arrow2")



colors = np.linspace(0, 1, len(patches))
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=1)
collection.set_array(np.array(colors))
print(collection)
ax.add_collection(collection)





plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.axis('equal')
plt.axis('off')


plt.imshow(img)
#plt.xlim(500, 550)
#plt.ylim(200, 30)
plt.show()