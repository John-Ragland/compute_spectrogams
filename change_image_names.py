import os

file_dir = '/Volumes/Ocean_Acoustics/Spectrograms/Southern_Hydrate/figures/'

file_list = os.listdir(file_dir)

for im in file_list:
    file_name = file_dir + im
    
    year = im[4:8]
    month = im[:3]

    if month == 'Jan':
        month_num = 1
    elif month == 'Feb':
        month_num = 2
    elif month == 'Mar':
        month_num = 3
    elif month == 'Apr':
        month_num = 4
    elif month == 'May':
        month_num = 5
    elif month == 'Jun':
        month_num = 6
    elif month == 'Jul':
        month_num = 7
    elif month == 'Aug':
        month_num = 8
    elif month == 'Sep':
        month_num = 9
    elif month == 'Oct':
        month_num = 10
    elif month == 'Nov':
        month_num = 11
    elif month == 'Dec':
        month_num = 12

    new_filename = file_dir + f'{year}_{month_num:02}.png'
    
    os.rename(file_name, new_filename)