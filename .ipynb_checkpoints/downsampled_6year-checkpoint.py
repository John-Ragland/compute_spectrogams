import pickle
import ooipy
import spec_tools
import numpy as np
from matplotlib import pyplot as plt

hydrophones = ['Axial_Base','Central_Caldera','Eastern_Caldera','Slope_Base','Southern_Hydrate']
for hydrophone in hydrophones:
    print(f'Calculating 6 Year Spectrogram for {hydrophone}')
    spec = spec_tools.downsample_for_figure(hydrophone)