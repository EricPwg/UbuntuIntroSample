# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 03:49:13 2018

@author: user
"""

api_keys = 'e777b17fd6e41bfc'
forcast_data_key = ['temp', 'dewpoint', 'humidity', 'wspd', 'wdir_deg', 'mslp']
forcast_num=240

from pylab import *

import urllib3
import json
import datetime

def list_double_reverse(data):
    t = list(data)
    tt = list(data)
    tt.reverse()
    t.extend(tt)
    return t

def draw_pic(pws):    
    while 1:
        r = urllib3.PoolManager()
        r = r.request('GET', 'http://api.wunderground.com/api/'+api_keys+'/hourly10day/q/pws:'+pws+'.json')
        data = r.data
        try:
            data = json.loads(data)
        except:
            continue
        try:
            tt = data['hourly_forecast']
            
        except:
            print('http://api.wunderground.com/api/e777b17fd6e41bfc/hourly10day/q/pws:'+pws+'.json'+' key error.')
            print(data)
            continue

        if len(data['hourly_forecast']) == forcast_num:
            break
        print('http://api.wunderground.com/api/e777b17fd6e41bfc/hourly10day/q/pws:'+pws+'.json'+' GET list of len '+str(len(data['hourly_forecast'])))
        time.sleep(10)
        print('retry at '+str(datetime.datetime.now()))
    
    temp = []
    dewpoint = []
    humidity = []
    wspd = []
    wdir_deg = []
    mslp = []
    
    temp_sig = []
    dewpoint_sig = []
    humidity_sig = []
    wspd_sig = []
    wdir_deg_sig = []
    mslp_sig = []
    
    temp_avg=[]
    dewpoint_avg=[]
    humidity_avg=[]
    wspd_avg=[]
    wdir_deg_avg=[]
    mslp_avg=[]
    
    for j in range(forcast_num):
        g = data['hourly_forecast'][j]
        temp.append(float(g['temp']['metric']))
        dewpoint.append(float(g['dewpoint']['metric']))
        humidity.append(float(g['humidity']))
        wspd.append(float(g['wspd']['metric']))
        wdir_deg.append(float(g['wdir']['degrees']))
        mslp.append(float(g['mslp']['metric']))
        
    f = open('analysis_'+pws+'.txt', 'r')
    f = f.readlines()
    mean1 = f[0].split()
    sigma1 = f[1].split()
    mean2 = f[2].split()
    sigma2 = f[3].split()
    mean3 = f[4].split()
    sigma3 = f[5].split()
    mean4 = f[6].split()
    sigma4 = f[7].split()
    mean5 = f[8].split()
    sigma5 = f[9].split()
    mean6 = f[10].split()
    sigma6 = f[11].split()
    
    for i in range(forcast_num):
        offset = temp[i]+float(mean1[i+1])
        var = float(sigma1[i+1])
        temp_avg.append(offset)
        temp_sig.append(var)
        
        offset = dewpoint[i]+float(mean2[i+1])
        var = float(sigma2[i+1])
        dewpoint_avg.append(offset)
        dewpoint_sig.append(var)
        
        offset = humidity[i]+float(mean3[i+1])
        var = float(sigma3[i+1])
        humidity_avg.append(offset)
        humidity_sig.append(var)
        
        offset = wspd[i]+float(mean4[i+1])
        var = float(sigma4[i+1])
        wspd_avg.append(offset)
        wspd_sig.append(var)
        
        offset = wdir_deg[i]+float(mean5[i+1])
        var = float(sigma5[i+1])
        wdir_deg_avg.append(offset)
        wdir_deg_sig.append(var)
        
        offset = mslp[i]+float(mean6[i+1])
        var = float(sigma6[i+1])
        mslp_avg.append(offset)
        mslp_sig.append(var)
    
    times_arr = [1 for i in range(240)]
    tt = [-1 for i in range(240)]
    times_arr.extend(tt)
    for i in range(240):
        times_arr.append
    
    figure(figsize=(30,10))
    xlabel_list=['Temperature', 'Dewpoint', 'Humidity', 'Wind Speed', 'Wind Direction', 'Pressure']
    data_list = [temp, dewpoint, humidity, wspd, wdir_deg, mslp]
    avg_list=[temp_avg, dewpoint_avg, humidity_avg, wspd_avg, wdir_deg_avg, mslp_avg]
    sig_list=[temp_sig, dewpoint_sig, humidity_sig, wspd_sig, wdir_deg_sig, mslp_sig]
    for k in range(6):
        subplot(2, 3, k+1)
        x_axis = [i for i in range(len(temp))]
        plot(x_axis, data_list[k], label='forcast')
        plot(x_axis, avg_list[k], 'r--', label='forcast correction')
        xt = list_double_reverse(x_axis)
        avgt = np.array(list_double_reverse(avg_list[k]))
        sigt = np.array(list_double_reverse(sig_list[k]))
        fill(xt, avgt+sigt*times_arr, 'g', alpha=0.3, label='forcast correction range')
        fill(xt, avgt+sigt*2*times_arr, 'g', alpha=0.3)
        title(xlabel_list[k]+' Forcast')
        xlabel('Hours')
        legend()
    
    suptitle(pws)
    
    savefig(pws+'.png')


#s = draw_pic(pws)


PWSf = open('PWS_list.txt', 'r')
PWSf = PWSf.readlines()

PWS=[]
for i in range(len(PWSf)):
    g = PWSf[i].split()
    PWS.append(g[0])

for i in range(len(PWS)):
    print(PWS[i])
    draw_pic(PWS[i])
