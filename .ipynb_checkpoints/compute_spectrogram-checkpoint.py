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


node = '/PC01A'
num_hours = 5

start_time_first = datetime.datetime(2017,7,13,23,0,0)

kstart = 0
for k in range(kstart,num_hours):
    start_time = start_time_first + timedelta(hours=k)
    end_time = start_time_first + timedelta(hours=k+1)
    print(f'Computing Spectrogram for {start_time} - {end_time}: {k}')
    print('   Downloading Data...')

    # Units are Pa
    hdata = hydrophone_request.get_acoustic_data(start_time, end_time, node)

    print('   Computing Spectrogram...')
    try:
        # Units of Spectrogram are (dB rel uPa)^2/Hz
        spec = hdata.compute_spectrogram(avg_time=60)
    except:
        print('   No Data for time segment')
        spec = None
    print('   Writing to File...')

    # Write to Pickle File
    filename = f"spectrogram{k:03}.pkl"
    with open(filename,'wb') as f:
        pickle.dump(spec, f)
