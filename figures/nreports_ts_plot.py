#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:43:22 2018

@author: iregon
"""
import json
import sys
import logging
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np

logging.getLogger('plt').setLevel(logging.INFO)
logging.getLogger('mpl').setLevel(logging.INFO)

# PARAMS ----------------------------------------------------------------------

DTMEAN = 1 #12

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
    config_file = sys.argv[1]
    
    with open(config_file) as cf:
        config = json.load(cf)
    
    file_data = config['file_data']
    file_out = config['file_out']
    year_init = int(config['year_init'])
    year_end = int(config['year_end'])
    
    data = pd.read_csv(file_data,delimiter='|',header = 0,index_col=[0],parse_dates=[0])
    
    y_med = data['0'].max()/2
    
    # Use min_periods argument in rolling if a gap needs to bo covered...
    f, ax = plt.subplots(1, 1,figsize=figsize)
    if '0.ships' in data.keys():
        nships=data['0.ships'].rolling(DTMEAN, center=True).mean()#.rolling(12, center=True)
    else:
        exit('No ships in dataset???')
    if '0.buoys' in data.keys():
        nbuoys=data['0.buoys'].rolling(DTMEAN, center=True).mean()#.rolling(12, center=True)
    else:
        logging.warning('Buoy count is zero')
        logging.info('0.ships: {}'.format(data['0.ships']))
        logging.info('0: {}'.format(data['0']))
        logging.info('equ: {}'.format(data['0.ships'].values!=data['0'].values))
        if any(data['0.ships'].values!=data['0'].values):exit('No buoyies and not all ships?')
        nbuoys=pd.Series(np.zeros_like(nships.values), index=nships.index, name='0.buoys')

    logging.info('nships: {}'.format(nships))
    logging.info('nb: {}'.format(nbuoys))
    logging.info('Sizes: {} (index), {} (nships), {} (nbuoys)'.format(nships.index.shape, nships.values.shape, nbuoys.values.shape))
    ax.stackplot(nships.index,nships.values,nbuoys.values, labels = ['ships','drifters'], colors=['grey','Gold'],alpha = 0.3)
    ax.plot(data['0'].rolling(12, center=True).mean(),label='__nolegend__',linewidth = 1,linestyle = ':',color = 'Black',alpha=0.7)
    
#    ax.axvline(x=datetime.datetime(1950,1,1),color='Black')
#    ax.text(datetime.datetime(1965,1,1),y_med,'Release 1',fontsize=16,style='italic')
#    ax.text(datetime.datetime(1890,1,1),y_med,'Release 2',fontsize=16,style='italic')
    
    ax.ticklabel_format(axis='y', style='sci',scilimits=(-3,4))
    ax.set_xlim(datetime.datetime(year_init,1,1),datetime.datetime(year_end,12,31))
    ax.grid(alpha=0.3,color='k',linestyle=':')
    ax.legend()
    ax.set_yscale('log')
    ax.set_ylabel('Number of reports')
    ax.set_xlabel('Time')
    f.tight_layout()
    plt.savefig(file_out,bbox_inches='tight',dpi = 300)
