import os
import sys

cwd = os.getcwd()
ooipy_dir = os.path.dirname(cwd) + '/ooipy'
sys.path.append(ooipy_dir)

from matplotlib import pyplot as plt
import datetime
import numpy as np
from obspy import read,Stream, Trace
from obspy.core import UTCDateTime

from obspy import read
import pickle
import scipy
from gwpy.timeseries import TimeSeries
import seaborn as sns

from ooipy.request import hydrophone_request
import gwpy

from datetime import timedelta

nodes = ['Axial_Base', 'Slope_Base', 'Southern_Hydrate']
years = [2015, 2016, 2017, 2018, 2019, 2020]

for node in nodes:
    for year in years:
        start_time_first = datetime.datetime(year,1,1,0,0,0)
        
        # set num of hours in year depending on leap
        if (year % 4) == 0:
            num_hours = 8784
        else:
            num_hours = 8760

        kstart = 0
        for k in range(kstart,num_hours):
            start_time = start_time_first + timedelta(hours=k)
            end_time = start_time_first + timedelta(hours=k+1)
            print(f'Computing Spectrogram for {node} | {start_time} - {end_time}: {k}')
            print('   Downloading Data...')
            hdata = hydrophone_request.get_acoustic_data_LF(start_time, end_time, node)
            print('   Computing Spectrogram...')
            try:
                spec = hdata.compute_spectrogram(avg_time=60)
            except:
                print('   No Data for time segment')
                spec = None
            print('   Writing to File...')

            # Write to Pickle File
            filename = "/Volumes/Ocean_Acoustics/Spectrograms/" +node+ "/" + str(year) +f"/spectrogram{k:03}.pkl"
            with open(filename,'wb') as f:
                pickle.dump(spec, f)

                
node = 'Eastern Caldera'

start_time = datetime.datetime(2016,6,1)
end_time = datetime.datetime(2016,8,1)