# Compute Spectrogram
This is a python package built on top of ooipy to compute long-term spectrograms.

The code is pretty messy and contains alot of hard coded specifics to my local environment, but
at least provides a good starting point for looping through large amounts of data.

## Where to start
- compute_spectrogram_lf.py
    - loops through low frequency data one hour at a time, downloads data from ooi and then computes PSDs for data
    - saves results in pickle file with following file structure
        - Year
            - pickle files for each hour
        - Year
            - pickle files for each hour
        - ... etc

- plot_spectrogram_from_file.ipynb
    - given a file structure of PSDs that is created with compute_spectrogram.py, it reads specified slice of data into memory and can plot this spectrogram
    - uses ooipy plotting functions (or xarray and hvplot)