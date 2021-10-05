import os
import sys

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

from tqdm import tqdm

import pandas as pd

def get_hour_index_array(leap=False):
    if leap:
        hours_in_month = np.array([0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])*24
    else:
        hours_in_month = np.array([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])*24
    hr_idx = []
    for k in range(13):
        hr_idx.append(sum(hours_in_month[:k+1]))

    return hr_idx

def merge(spec_start, spec_end, spec_dir, verbose=True):
    '''
    merge seperate spectrogram files to single spectrogram instance
    Parameters
    ----------
    spec_start : int
        index of spec start file
    spec_end : int
        index of spec end file
    spec_dir : str
        full path where spectrograms are located
    verbose : bool
        whether to print updates or not
    '''
    # add slash to end of spec_dir if it doesn't exit
    if spec_dir[-1] != '/':
        spec_dir += '/'

    # TODO this is still broken
    # set spec_end to largest possible if input is larger than possible
    if (int(spec_dir[-5:-1]) % 4 == 0) & (spec_end >= 8784):
        spec_end = 8783
        #print('invalid spec_end')
    elif (int(spec_dir[-5:-1]) % 4 != 0) & (spec_end >= 8760):
        spec_end = 8759
        #print('invalid spec_end')

    time = []

    for k in tqdm(range(spec_start,spec_end), disable=(not verbose)):
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

    try:
        values
        times
        freq
    except NameError:
        # fft size is hard coded!
        values = np.empty((1,512,))
        values[:] = np.nan
        freq = np.empty(512)
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
    hr_idx = get_hour_index_array(leap)
    
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
    hr_idx = get_hour_index_array(leap=False)
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

def downsample_for_figure(hydrophone, avg_len = 12):
    '''
    takes spectrogram for hydrophone and averages in 12 hour increments so that
    6 year long figure can be created. Spectrogram file is saved in hydrophone
    file directory
    
    Parameters
    ----------
    hydrophone : str
        'Axial_Base', 'Central_Caldera', 'Eastern_Caldera', 'Slope_Base',
        and 'Southern_Hydrate' are acceptable inputs. Specificies hydrophone
    avg_len : float
        length of average period in hours

    Returns
    -------
    spec : ooipy.hydrophone.basic.Spectrogram
        spectrogram data object
    '''
    # Check that hydrophone is valid
    hydrophones = ['Axial_Base', 'Central_Caldera', 'Eastern_Caldera', 'Slope_Base', 'Southern_Hydrate']
    if hydrophone not in hydrophones:
        raise Exception('invalid hydrophone string')

    spec_values = []
    spec_times = []

    years = [2015, 2016, 2017, 2018, 2019, 2020]
    
    for year in years:
        print('', end='\r')
        print(f'    Averaging {year}...')
        spec_dir = f'/Volumes/Ocean_Acoustics/Spectrograms/{hydrophone}/{year}/'
        
        if year % 4 == 0:
            end_idx = 8782
        else:
            end_idx = 8758
        
        for k in tqdm(range(0,end_idx,avg_len)):
            start = k
            end = k + avg_len-1
            _, _, values = merge(start, end, spec_dir, verbose=False)
            
            #try:
            spec_values.append(np.mean(values,axis=0))

            # calculate time from hour value
            time = pd.Timestamp(f'{year}-01-01') + pd.Timedelta(hours=start)
            time = time.to_pydatetime()
            spec_times.append(time)
            
            #except:
            #    spec_values.append(np.mean(values, axis=0))
            #    spec_times.append(np.nan)
    
    
    spec_values_np = np.array(spec_values)
    spec_times_np = np.array(spec_times)

    freq = np.linspace(0, 100, spec_values_np.shape[1])
    spec = ooipy.hydrophone.basic.Spectrogram(spec_times_np, freq, spec_values_np)

    filename = f'/Volumes/Ocean_Acoustics/Spectrograms/{hydrophone}/6_year_spectrogram.pkl'
    
    with open(filename, 'wb') as f:
        pickle.dump(spec, f)

    return spec

def monthly_psds(years, months, nodes, savefig=True):
    '''
    calculate and plot average psds for each month
    '''
    
    for node in nodes:
        for year in years:
            for month in months:
                psd_dir = f'/Volumes/Ocean_Acoustics/Spectrograms/{node}/psds/'
                print(f'Merging for {node}, {year}-{month}...\n')

                month_hours = get_hour_index_array(year%4==0)
                spec_start, spec_end = month_hours[month-1], month_hours[month]
                spec_dir = f'/Volumes/Ocean_Acoustics/Spectrograms/{node}/{year}/'
                

                _, freq, values = merge(spec_start, spec_end, spec_dir)

                PSD = np.mean(values, axis=0)

                fig = plt.figure(figsize=(7,5))
                ax = plt.axes()
                plt.sca(ax)
                plt.plot(freq, PSD)
                plt.grid()
                plt.ylabel('Power (dB)')
                plt.xlabel('frequency (Hz)')
                plt.grid()
                plt.xlim([0, 100])
            
                im_name = f'{year}-{month}_PSD.png'
                image_dir = psd_dir + im_name

                if savefig:
                    fig.savefig(image_dir, dpi=300)
                    plt.close()
                else:
                    return fig, ax