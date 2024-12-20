#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:43:22 2018

@author: iregon
"""
import json
import sys
import os
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
import pandas as pd
import datetime


logging.getLogger('plt').setLevel(logging.INFO)
logging.getLogger('mpl').setLevel(logging.INFO)


REPORT_QUALITY = ['0','1','2']
# PARAMS ----------------------------------------------------------------------
# Set plotting defaults
plt.rc('legend',**{'fontsize':10})        # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=9)    # fontsize of the tick labels
plt.rc('ytick', labelsize=9)    # fontsize of the tick labels
plt.rc('figure', titlesize=14)  # fontsize of the figure title

figsize = (7,3)
# END PARAMS ------------------------------------------------------------------


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    
    sid_dck = sys.argv[1]
    config_file = sys.argv[2]
    
    with open(config_file) as cf:
        config = json.load(cf)
    
    file_data = os.path.join(config['dir_data'],sid_dck,config['file_data'])
    file_out = os.path.join(config['dir_out'],sid_dck,sid_dck+'_'+config['file_out'])

    data = pd.read_csv(file_data,delimiter='|',header = 0,index_col=[0],parse_dates=[0])
   
    # Complete all dup status
    for status in REPORT_QUALITY:
        if status not in data.columns:
            data[status] = pd.Series(index=data.index)
            data[status] = 0
        else:
            data[status].fillna(0)
       # data[status] = pd.Series(index=data.index) if status not in data.columns else data[status]
    
    data['nreports.ships'].fillna(0)

    f, ax = plt.subplots(1, 1,figsize=figsize)
    
    width = 24.
    labels = data.index

    data0 = 100*data['0']/data['nreports']
    ax.bar(labels, data0, width, label='qc ok',color='Grey')

    data1 = 100*data['1']/data['nreports']
    ax.bar(labels, data1, width, bottom=data0, label='qc failed',color='Red')
  
    data2 = 100*data['2']/data['nreports']
    ax.bar(labels, data2, width, bottom=data0+data1, label='not checked',color='Yellow')

    ax2=ax.twinx()
    ax2.plot(data['nreports.ships'],linewidth = 1, linestyle='-',marker='.', color = 'Black',alpha=0.7)

    ax.ticklabel_format(axis='y', style='sci',scilimits=(-3,4))
    ax.set_ylim(0,100)
    ax.grid(alpha=0.3,color='k',linestyle=':')
    ax.legend(loc='lower left',facecolor = 'white')
    ax.set_ylabel('Percent of reports')
    ax2.set_ylabel('total muber of ship reports')
    ax.set_xlabel('Time')
    plt.title('SID/Deck: '+sid_dck)
    f.tight_layout()
    plt.savefig(file_out,bbox_inches='tight',dpi = 300)
