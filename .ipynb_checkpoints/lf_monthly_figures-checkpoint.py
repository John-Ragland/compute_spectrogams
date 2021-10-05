import numpy as np
import spec_tools

file_path_base = "/Volumes/Ocean_Acoustics/Spectrograms/"
years = ['2015', '2016', '2017', '2018', '2019', '2020']
nodes = ['Axial_Base','Central_Caldera','Eastern_Caldera','Slope_Base','Southern_Hydrate']
for node in nodes:
    for year in years:
        spec_path = file_path_base + node + '/' + year
        imag_path = file_path_base + node + '/figures/'

        spec_tools.monthly_specs(spec_path, imag_path, node)

# spec_tools.monthly_specs(file_path, 'Axial_Base')