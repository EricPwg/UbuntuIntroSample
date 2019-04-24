# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 04:28:16 2018

@author: user
"""

api_keys = 'e777b17fd6e41bfc'
start_time = datetime.datetime(2017, 12, 19)

import urllib3
import json
import fnmatch
import os
import datetime
import time
import numpy as np



history_data_key = ['tempm', 'dewptm', 'hum', 'wspdm', 'wdird', 'pressurem']
forcast_data_key = ['temp', 'dewpoint', 'humidity', 'wspd', 'wdir_deg', 'mslp']
forcast_data_index=[4, 5, 19, 6, 21, 12]
forcast_data_num = 23


now_time = datetime.datetime.now()
#now_time = datetime.datetime(2017, 12, 20)
days = now_time - start_time
days = days.days+1

def load_data(data):
    r={'time':data['date']['pretty']}
    for i in range(len(history_data_key)):
        r[forcast_data_key[i]] = float(data[history_data_key[i]])
    return r

def get_history(date, pws):
    url = 'http://api.wunderground.com/api/'+api_keys+'/history_'+date+'/q/pws:'+pws+'.json'
    count = 0
    while 1:
        r = urllib3.PoolManager()
        r = r.request('GET', url)
        data = r.data
        try:
            data = json.loads(data)
        except:
            continue
        try:
            tt = data['history']['observations']
        except:
            print(url+' key error.')
            print(data)
            continue
        if len(data['history']['observations']) > 0:
            count = 0
            break
        if count > 10:
            count = 0
            break
        print(url+' GET list of len '+str(len(data['history']['observations'])))
        time.sleep(30)
        print('retry at '+str(datetime.datetime.now()))
        count = count+1
        
    data = data['history']['observations']
    
    result = []
    
    hour_pointer = 0
    
    for i in range(len(data)):
        g = data[i]
        if int(g['date']['hour']) == hour_pointer:
            tt = load_data(g)
            result.append(tt)
            hour_pointer = hour_pointer+1
        else:
            pass
    print('lenght of result is '+str(len(result)))
    return result

def analysis(pws, forcast_file):
    results = {}
    observations_data = {}
    t_dict=[]
    for i in range(240):
        t_dict.append([])
        
    for i in range(len(forcast_data_key)):
        results[forcast_data_key[i]] = [[] for i in range(240)]
    
    for i in range(days):
        get_date = (start_time+datetime.timedelta(i)).strftime('%Y%m%d')
        observations_data[get_date] = get_history(get_date, pws)
        print('get data of '+pws+' on date '+get_date)
        print()
        time.sleep(10)
    
    for i in range(len(forcast_file)):
    #for i in range(1):
        f = open(forcast_file[i], 'r')
        f = f.readlines()
        print('open file '+forcast_file[i]+' success/')
        pws_index = 0
        for j in range(1, len(f)):
            if f[j].split()[0] == pws:
                pws_index = j
                break
        if pws_index == 0:
            continue
        g = f[pws_index].split('\t')
        for j in range(int(len(g)/forcast_data_num)):
            forcast_date = g[forcast_data_num*j+1]+g[forcast_data_num*j+2].zfill(2)+g[forcast_data_num*j+3].zfill(2)
            forcast_hour = g[forcast_data_num*j+4]
            if not forcast_date in observations_data.keys():
                continue
            data_list = observations_data[forcast_date]
            if len(data_list) <= int(forcast_hour):
                continue
            data_list = data_list[int(forcast_hour)]
            for k in range(len(forcast_data_index)):
                delta = data_list[forcast_data_key[k]]-float(g[forcast_data_num*j+1+forcast_data_index[k]])
                if k == 4 and np.abs(delta) > 180:
                    delta = (delta-360)%180
                if np.abs(delta) > 360:
                    continue
                results[forcast_data_key[k]][j].append(delta)
    c = open('analysis_'+pws+'.txt', 'w')
    for i in range(len(forcast_data_key)):
        c.write(forcast_data_key[i]+'_mean\t')
        for j in range(240):
            t = np.array(results[forcast_data_key[i]][j])
            mean = np.mean(t)
            c.write(str(round(mean, 3))+'\t')
        c.write('\n')
        c.write(forcast_data_key[i]+'_sigma\t')
        for j in range(240):
            t = np.array(results[forcast_data_key[i]][j])
            var = np.var(t)
            c.write(str(round(np.sqrt(var), 3))+'\t')
        c.write('\n')
    c.close()
        
        
    return results, observations_data



#result = get_history('20180106', 'IHSINCHU11')

forcast_file = [file for file in os.listdir('.') if fnmatch.fnmatch(file, '201*.txt')]

PWSf = open('PWS_list.txt', 'r')
PWSf = PWSf.readlines()

PWS=[]
for i in range(len(PWSf)):
    g = PWSf[i].split()
    PWS.append(g[0])


for i in range(len(PWS)):
    print('Start analysis pws:'+PWS[i])
    re, ob = analysis(PWS[i], forcast_file)
    