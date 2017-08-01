

#------------------------------------------------------------------------------
#   Getting Started
#------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

print('\n' * 5)
print('Loading data...')


#--------------------------------------------------------------------------
#   Load Trip Data
#--------------------------------------------------------------------------
try:
    print('Loading Trip Data Files')
    file_path_slug = '../../datasets/bayareabikeshare/201*_trip_data.csv'

    # glob all files
    file_list = glob(file_path_slug)

    counter = 1
    chunks = []
    for file in file_list:
        print('\tReading file [' + str(counter) + ' of ' + str(len(file_list)) + ']\t ' + str(file))

        # import file in chunks to temp DataFrame
        # print('\treading chunks...')
        for chunk in pd.read_csv(file, chunksize=10000, iterator=True):

            chunk = chunk.set_index('Trip ID')

            chunks.append(chunk)

        # print('\tfinished file!')
        counter += 1

    # status = pd.concat(chunks, ignore_index=True)
    trips = pd.concat(chunks)


    # print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')

#--------------------------------------------------------------------------
#   Load Station Data
#--------------------------------------------------------------------------
try:
    print('Loading Station Data Files')
    file_path_slug = '../../datasets/bayareabikeshare/201*_station_data.csv'

    # glob all files
    file_list = glob(file_path_slug)

    counter = 1
    chunks = []
    for file in file_list:
        print('\tReading file [' + str(counter) + ' of ' + str(len(file_list)) + ']\t ' + str(file))

        # import file in chunks to temp DataFrame
        # print('\treading chunks...')
        for chunk in pd.read_csv(file, chunksize=10000, iterator=True):

            chunks.append(chunk)

        # print('\tfinished file!')
        counter += 1

    stations = pd.concat(chunks, ignore_index=True)
    # stations = pd.concat(chunks)


    # print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')

print('#' * 80)


#------------------------------------------------------------------------------
#   Data Cleanup
#------------------------------------------------------------------------------
print('Cleaning Station Data..')

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

#   cleanup column names
new_cols = []
for col in trips.columns:
    new_col = col.replace(' ', '_').lower()
    new_cols.append(new_col)
trips.columns = new_cols

#   prune down just columns we want to keep
important_cols = ['duration', 'start_date', 'start_terminal', 'end_date', 'end_terminal', 'bike_#', 'subscriber_type', 'zip_code']
trips = trips[important_cols]

print('\tfinished!')
print('#' * 80)


#------------------------------------------------------------------------------
#   Append columns of useful information
#------------------------------------------------------------------------------
print('Appending some useful columns to trips...')

#   create duration_minutes column
trips['duration_minutes'] = trips['duration'] / 60.

#   build station_id : landmark dict
landmark_dict = dict(zip(stations['station_id'].astype(int), stations['landmark'].str.lower().str.replace(' ', '_')))

# add 'start_landmark' and 'end_landmark' columns to trips
trips['start_landmark'] = trips['start_terminal']
trips = trips.replace({'start_landmark':landmark_dict})

trips['end_landmark'] = trips['end_terminal']
trips = trips.replace({'end_landmark':landmark_dict})



# #   Select only trips to and from different landmark areas
# trips = trips[trips.loc[:,'start_landmark'] != trips.loc[:,'end_landmark']]

# #   Select only trips in or out but not within San Francsico
# trips = trips[ (trips.loc[:,'start_landmark'] == 'san_francisco') | (trips.loc[:,'end_landmark'] == 'san_francisco') ]


# # look at unique values in each column
# print('#' * 80)
# print('#\tColumns and unique values')
# detail_cols = ['duration', 'start_terminal', 'end_terminal', 'subscriber_type', 'zip_code', 'start_landmark', 'end_landmark']
# for col in detail_cols:
#     print('Column : ' + col + '\t' + str(len(pd.unique(trips[col]))))
#     print(pd.unique(trips[col]))
#     print()


#   Select only trips within each landmark area
trips_mountain_view = trips[ (trips.loc[:,'start_landmark'] == 'mountain_view') & (trips.loc[:,'end_landmark'] == 'mountain_view') ]
trips_palo_alto = trips[ (trips.loc[:,'start_landmark'] == 'palo_alto') & (trips.loc[:,'end_landmark'] == 'palo_alto') ]
trips_redwood_city = trips[ (trips.loc[:,'start_landmark'] == 'redwood_city') & (trips.loc[:,'end_landmark'] == 'redwood_city') ]
trips_san_jose = trips[ (trips.loc[:,'start_landmark'] == 'san_jose') & (trips.loc[:,'end_landmark'] == 'san_jose') ]
trips_san_francisco = trips[ (trips.loc[:,'start_landmark'] == 'san_francisco') & (trips.loc[:,'end_landmark'] == 'san_francisco') ]


print('\tfinished!')
print('#' * 80)

# print(' ---- HEAD ---- ')
# print(trips.head(20))
#
# print(' ---- TAIL ---- ')
# print(trips.tail(20))
#
# print(' ---- SHAPE ---- ')
# print(trips.shape)



#------------------------------------------------------------------------------
#   Statistical Analysis
#------------------------------------------------------------------------------


print('trips_mountain_view:\t' + str(trips_mountain_view.shape[0]))
print('trips_palo_alto:\t' + str(trips_palo_alto.shape[0]))
print('trips_redwood_city:\t' + str(trips_redwood_city.shape[0]))
print('trips_san_jose:\t\t' + str(trips_san_jose.shape[0]))
print('trips_san_francisco:\t' + str(trips_san_francisco.shape[0]))



#   EOF
