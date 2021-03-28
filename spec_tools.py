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

import ooipy
from ooipy.request import hydrophone_request
from ooipy.hydrophone import basic
import gwpy

import plotly.express as px
import progressbar
from scipy import signal

import progressbar
import time as tm

def get_hour_index(leap=False):
    if leap:
        hours_in_month = np.array([0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])*24
    else:
        hours_in_month = np.array([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])*24
    hr_idx = []
    for k in range(13):
        hr_idx.append(sum(hours_in_month[:k+1]))

    return hr_idx
    
def merge(spec_start, spec_end, spec_dir):
    bar = progressbar.ProgressBar(maxval=spec_end-spec_start, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    time = []

    for k in range(spec_start,spec_end):
        # Read specific spectrogram file
        file_path = file_path = spec_dir + f"/spectrogram{k:03}.pkl"
        try:
            with open(file_path, 'rb') as f:
                spec = pickle.load(f)
            spec.time
        except:
            continue
        time_UTC = spec.time



        # Check if freq variable exist
        try:
            freq
        except NameError:
            freq = spec.freq

        # Change format of times to datetime
        for n in range(len(time_UTC)):
            if n == 0:
                if type(time_UTC[n]) == datetime.datetime:
                    time = [time_UTC[n]]
                else:
                    time = [time_UTC[n].datetime]
            else:
                if type(time_UTC[n]) == datetime.datetime:
                    time.append(time_UTC[n])
                else:
                    time.append(time_UTC[n].datetime)

        try:
            values
            times
        except NameError:
            values = spec.values
            times = np.asarray(time)
        else:
            values = np.vstack((values,spec.values))
            times = np.hstack((times,np.asarray(time)))
        bar.update(k- spec_start)

    try:
        values
        times
        freq
    except NameError:
        values = np.empty((1,2049,))
        values[:] = np.nan
        freq = np.empty(2049)
        freq[:] = np.nan
        times = np.nan

    return times, freq, values

def monthly_specs(spec_dir, imag_dir, node):
    
    year = int(spec_dir[-4:])

    if year % 4 == 0:
        leap = True
    else:
        leap = False

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    hr_idx = get_hour_index(leap)
    
    for k in range(12):
        print(f'Merging {node} Spectrograms for {months[k]}, {str(year)}...')

        image_path = imag_dir + months[k] + '_'  + str(year) + '.png'
        tm.sleep(0.2)
        times, freq, values = merge(hr_idx[k],hr_idx[k+1],spec_dir)

        try:
            # Create Spectrogram Object
            spec_full = basic.Spectrogram(times, freq, values)
        
            ooipy.tools.ooiplotlib.plot_spectrogram(
                spec_full, xlabel_rot=30,res_reduction_time=100, fmax=100, vmax = 80, vmin = 20,
                filename=image_path, save=True, plot=False)
        except:
            continue
    return

def create_all_specs():
    spec_dirs = [
        # "/Volumns/John's Passport/Specrograms/Eastern_Caldera/2016"
        # "/Volumes/John's Passport/Spectrograms/Eastern_Caldera/2017",
        # "/Volumes/John's Passport/Spectrograms/Eastern_Caldera/2018",
        "/Volumes/John's Passport/Spectrograms/Central_Caldera/2016",
        "/Volumes/John's Passport/Spectrograms/Central_Caldera/2017",
        "/Volumes/John's Passport/Spectrograms/Central_Caldera/2018"
        ]

    for k in range(5):
        monthly_specs(spec_dirs[k])
        plt.close('all')
    return

def yearlong_specs():
    spec_dirs = [
        "/Volumns/John's Passport/Specrograms/Eastern_Caldera/2016"
        "/Volumes/John's Passport/Spectrograms/Eastern_Caldera/2017",
        "/Volumes/John's Passport/Spectrograms/Eastern_Caldera/2018",
        "/Volumes/John's Passport/Spectrograms/Central_Caldera/2016",
        "/Volumes/John's Passport/Spectrograms/Central_Caldera/2017",
        "/Volumes/John's Passport/Spectrograms/Central_Caldera/2018"
        ]
    
    times, freq, values = merge(0,8759, spec_dirs[0])

    # Create Spectrogram Object
    spec_full = basic.Spectrogram(times, freq, values)
    image_path = 'eastern_caldera_2016.png'

    ooipy.tools.ooiplotlib.plot_spectrogram(
        spec_full, xlabel_rot=30,res_reduction_time=600, fmax=100,
        filename=image_path,save=True, dpi=300)
    
    return

def single_month(spec_dir, month):
    k = month -1
    hr_idx = get_hour_index(leap=False)
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    print(f'Merging Spectrograms for {months[k]}, {spec_dir[-20:-5]}, {spec_dir[-4:]}...')
    tm.sleep(0.5)
    times, freq, values = merge(hr_idx[k],hr_idx[k+1],spec_dir)

    np.nan_to_num(values,copy=False,nan=0)

    # Create Spectrogram Object
    spec_full = basic.Spectrogram(times, freq, values)

    image_path = 'monthly_figures' + spec_dir[-21:] + '/' + months[k] + '.png'
    ooipy.tools.ooiplotlib.plot_spectrogram(
    spec_full, xlabel_rot=30,res_reduction_time=50, fmax=100,
    filename=image_path,save=True, dpi=300)
