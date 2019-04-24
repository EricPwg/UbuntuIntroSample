# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 20:57:43 2018

@author: user
"""


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
    
    temp_sig = []
    dewpoint_sig = []
    humidity_sig = []
    wspd_sig = []
    wdir_deg_sig = []
    mslp_sig = []
    
    temp_avg=[0]
    dewpoint_avg=[0]
    humidity_avg=[0]
    wspd_avg=[0]
    wdir_deg_avg=[0]
    mslp_avg=[0]
        
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
        offset = float(mean1[i+1])
        var = float(sigma1[i+1])
        temp_avg.append(offset)
        temp_sig.append(var)
        
        offset = float(mean2[i+1])
        var = float(sigma2[i+1])
        dewpoint_avg.append(offset)
        dewpoint_sig.append(var)
        
        offset = float(mean3[i+1])
        var = float(sigma3[i+1])
        humidity_avg.append(offset)
        humidity_sig.append(var)
        
        offset = float(mean4[i+1])
        var = float(sigma4[i+1])
        wspd_avg.append(offset)
        wspd_sig.append(var)
        
        offset = float(mean5[i+1])
        var = float(sigma5[i+1])
        wdir_deg_avg.append(offset)
        wdir_deg_sig.append(var)
        
        offset = float(mean6[i+1])
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
    avg_list=[temp_avg, dewpoint_avg, humidity_avg, wspd_avg, wdir_deg_avg, mslp_avg]
    sig_list=[temp_sig, dewpoint_sig, humidity_sig, wspd_sig, wdir_deg_sig, mslp_sig]
    for k in range(6):
        subplot(2, 3, k+1)
        x_axis = [i+1 for i in range(len(sig_list[k]))]
        plot(x_axis, sig_list[k], label='Sigma')
        x_axis = [i for i in range(len(avg_list[k]))]
        x_axis.append(240)
        avg_list[k].append(0)
        fill(x_axis, avg_list[k], 'y', alpha=0.3, label='Average')
        title(xlabel_list[k]+' Result')
        xlabel('Hours')
        legend()
    
    suptitle(pws)
    
    savefig(pws+'_result.png')


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

#['I1236', 'ITAIWANK2', 'I1419', 'IU6843U52', 'IHSINCHU11', 'IMIAOLI4', 'ITAICHUN7', 'I1267', 'ILIUJIAD2', 'ITAINANC2', 'I1270', 'IU53F0U78', 'I1912', 'I5286', 'IHUALIEN4', 'IHUALIEN3', 'I5291', 'IKINMENC2']