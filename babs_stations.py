

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#   Import stock data

#------------------------------------------------------------------------------
#   Load Data Sets
#------------------------------------------------------------------------------
print('Loading data...')

try:
    stations_path_01 = '../../datasets/bayareabikeshare/201402_station_data.csv'
    stations_01 = pd.read_csv(stations_path_01, header=0)

    stations_path_02 = '../../datasets/bayareabikeshare/201408_station_data.csv'
    stations_02 = pd.read_csv(stations_path_02, header=0)

    stations_path_03 = '../../datasets/bayareabikeshare/201508_station_data.csv'
    stations_03 = pd.read_csv(stations_path_03, header=0)

    stations_path_04 = '../../datasets/bayareabikeshare/201608_station_data.csv'
    stations_04 = pd.read_csv(stations_path_04, header=0)

    print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')


print('\n\n')


print('#' * 80)
#------------------------------------------------------------------------------
#   Data Prep
#------------------------------------------------------------------------------

print('Data cleanup started...')

#   merge dataframes
frames = [stations_01, stations_02, stations_03, stations_04]
stations = pd.concat(frames, ignore_index=True)

#   drop empty rows
stations.dropna(how="all", inplace=True)

#   convert station IDs to strings
stations['station_id'] = stations['station_id'].astype(int)
stations['station_id'] = stations['station_id'].astype(str)

#   convert dockcount to int, no such thing as a partial dock
stations['dockcount'] = stations['dockcount'].astype(int)

#   convert installation to datetime
stations['installation'] = pd.to_datetime(stations['installation'])

#   drop duplicate rows and reindex
stations = stations.drop_duplicates(keep='first')
stations.reset_index(inplace=True, drop=True)

print('\tComplete!')
print('#' * 80)
#------------------------------------------------------------------------------
#   Statistical Analysis
#------------------------------------------------------------------------------

#look at unique values in each column
print('#' * 80)
print('#\tColumns and unique values')
important_cols = ['station_id', 'name', 'dockcount', 'landmark', 'installation']
for col in important_cols:
    print('Column : ' + col + '\t' + str(len(pd.unique(stations[col]))))
    print(pd.unique(stations[col]))
    print()

print('#\tHEAD')
print(stations.head())
print('#' * 80)

print('#\tTAIL')
print(stations.tail())
print('#' * 80)

print('#\tINFO')
print(stations.info())
print('#' * 80)

print('#\tDESCRIBE')
print(stations.describe())
print('#' * 80)
print('#' * 80)
print('#' * 80)

print(stations.head(275))

#------------------------------------------------------------------------------
#   Split Up by Areas
#------------------------------------------------------------------------------
areas = pd.unique(stations['landmark'])

stations_SanJose = stations.loc[stations['landmark'] == 'San Jose']
print('\t>>>\tSan Jose')
print(stations_SanJose.info())
station_IDs_SanJose = pd.unique(stations_SanJose['station_id'])
print(station_IDs_SanJose)
print('#' * 80)

stations_RedwoodCity = stations.loc[stations['landmark'] == 'Redwood City']
print('\t>>>\tRedwood City')
print(stations_RedwoodCity.info())
station_IDs_RedwoodCity = pd.unique(stations_RedwoodCity['station_id'])
print(station_IDs_RedwoodCity)
print('#' * 80)

stations_MountainView = stations.loc[stations['landmark'] == 'Mountain View']
print('\t>>>\tMountain View')
print(stations_MountainView.info())
station_IDs_MountainView = pd.unique(stations_MountainView['station_id'])
print(station_IDs_MountainView)
print('#' * 80)

stations_PaloAlto = stations.loc[stations['landmark'] == 'Palo Alto']
print('\t>>>\tPalo Alto')
print(stations_PaloAlto.info())
station_IDs_PaloAlto = pd.unique(stations_PaloAlto['station_id'])
print(station_IDs_PaloAlto)
print('#' * 80)

stations_SanFrancisco = stations.loc[stations['landmark'] == 'San Francisco']
print('\t>>>\tSan Francisco')
print(stations_SanFrancisco.info())
station_IDs_SanFrancisco = pd.unique(stations_SanFrancisco['station_id'])
print(station_IDs_SanFrancisco)
print('#' * 80)



#------------------------------------------------------------------------------
#   Data Visualization
#------------------------------------------------------------------------------


# 25,30,33
#   EOF
