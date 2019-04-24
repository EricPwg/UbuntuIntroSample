# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:34:00 2017

@author: user
"""

api_keys = 'e777b17fd6e41bfc'
get_data_time = 1

import urllib3
import json
import datetime
import time

forcast_num=240

str_int_list=['fctcode', 'sky', 'uvi', 'humidity', 'pop']
str_str_list=['condition', 'icon', 'wx']
dict_list=['temp', 'dewpoint', 'wspd', 'windchill', 'heatindex', 'feelslike', 'qpf', 'snow', 'mslp']
dict_wind='wdir'

fcttime_list=['year', 'mon', 'mday', 'hour']
station_id='PWSid'



def write_head(f):
    f.write(station_id)
    for kk in range(forcast_num):
        for i in range(len(fcttime_list)):
            f.write('\t'+fcttime_list[i])
        for i in range(len(dict_list)):
            f.write('\t'+dict_list[i])
        for i in range(len(str_str_list)):
            f.write('\t'+str_str_list[i])
        for i in range(len(str_int_list)):
            f.write('\t'+str_int_list[i])
        f.write('\t'+dict_wind+'_deg'+'\t'+dict_wind+'_dir')
    f.write('\n')

def data_split(dict_data, f):
    for i in range(len(fcttime_list)):
        f.write('\t'+dict_data['FCTTIME'][fcttime_list[i]])
    for i in range(len(dict_list)):
        f.write('\t'+dict_data[dict_list[i]]['metric'])
    for i in range(len(str_str_list)):
        f.write('\t'+dict_data[str_str_list[i]])
    for i in range(len(str_int_list)):
        f.write('\t'+dict_data[str_int_list[i]])
    f.write('\t'+dict_data['wdir']['degrees']+'\t'+dict_data['wdir']['dir'])
        

def data_get():
    PWSf = open('PWS_list.txt', 'r')
    PWSf = PWSf.readlines()
    
    PWS=[]
    
    file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H')+'.txt'
    print('Start get data > '+file_name)
    f = open(file_name, 'w')
    write_head(f)
    
    for i in range(len(PWSf)):
        g = PWSf[i].split()
        PWS.append(g[0])
        
    for i in range(len(PWS)):
        while 1:
            r = urllib3.PoolManager()
            r = r.request('GET', 'http://api.wunderground.com/api/'+api_keys+'/hourly10day/q/pws:'+PWS[i]+'.json')
            data = r.data
            try:
                data = json.loads(data)
            except:
                continue
            try:
                tt = data['hourly_forecast']
                
            except:
                print('http://api.wunderground.com/api/'+api_keys+'/hourly10day/q/pws:'+PWS[i]+'.json'+' key error.')
                print(data)
                continue

            if len(data['hourly_forecast']) == forcast_num:
                break
            print('http://api.wunderground.com/api/'+api_keys+'/hourly10day/q/pws:'+PWS[i]+'.json'+' GET list of len '+str(len(data['hourly_forecast'])))
            time.sleep(10)
            print('retry at '+str(datetime.datetime.now()))
        #print(data)
        f.write(PWS[i])
        for j in range(forcast_num):
            data_split(data['hourly_forecast'][j], f)
        f.write('\n')
        print('*', end='')
        time.sleep(10)
    f.close()
    print()


data_get()
print('Get test data success')
while 1:
    
    m = int(datetime.datetime.now().strftime('%M'))
    if m == get_data_time:
        print()
        data_get()
        print('Data get success')
    elif m == (get_data_time+30)%60:
        print('.', end='')
        print()
    else:
        print('.', end='')
    time.sleep(59.5)
