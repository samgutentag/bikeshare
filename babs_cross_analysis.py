

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

#------------------------------------------------------------------------------
#   Load Data Sets
#------------------------------------------------------------------------------
print('\n\n')
print('\n\n')
print('Loading data...')
try:

    #--------------------------------------------------------------------------
    #   Trip Data
    #--------------------------------------------------------------------------
    print('Loading Trip Data Files')
    file_path_slug = '../../datasets/bayareabikeshare/*_trip_data.csv'

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

try:

    #--------------------------------------------------------------------------
    #   Station Data
    #--------------------------------------------------------------------------
    print('Loading Station Data Files')
    file_path_slug = '../../datasets/bayareabikeshare/*_station_data.csv'

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


# #------------------------------------------------------------------------------
# #   Data Quick Look - Import
# #------------------------------------------------------------------------------
#
# print('''#------------------------------------------------------------------------------
# #   Data Quick Look - Import
# #------------------------------------------------------------------------------''')
#
# print('*' * 80)
# print('stations')
# print(stations.head())
# print(stations.info())
#
# # print('*' * 80)
# # print('trips')
# # print(trips.head())
# # print(trips.info())


#------------------------------------------------------------------------------
#   Data Cleanup
#------------------------------------------------------------------------------

print('cleanup of Station Data')

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

#   Map stations['landmark'] to trips based on station_id



# print('*' * 80)
# print('stations')
# print(stations.head())
# print(stations.info())

#   cleanup column names
new_cols = []
for col in trips.columns:
    new_col = col.replace(' ', '_').lower()
    new_cols.append(new_col)
trips.columns = new_cols

#   prune down just columns we want to keep
important_cols = ['duration', 'start_date', 'start_terminal', 'end_date', 'end_terminal', 'bike_#', 'subscriber_type', 'zip_code']
trips = trips[important_cols]


#   subset trips that leave and return to same terminal
trips = trips[trips.loc[:,'start_terminal'] != trips.loc[:,'end_terminal']]

#   create duration_minutes column
trips['duration_minutes'] = trips['duration'] / 60.

# print('-' * 80)
# print('-' * 80)
# print('-' * 80)


# subset trips dataframe for testing
#   prune data set by start stations
# trips = trips[trips.loc[:,'start_terminal'] < 23]
# trips = trips[trips.loc[:,'start_terminal'] > 15]

#   prune data set by duration
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24

#   subset trips that leave and return to same terminal
# trips = trips[trips.loc[:,'start_terminal'] == trips.loc[:,'end_terminal']]


# trips = trips[trips['duration'] < hour]
# trips = trips[trips['duration'] > 10 * minute]
trips = trips[trips['duration'] > 2 * hour]
trips = trips[trips['duration'] < 10 * hour]

#   build station_id : landmark dict
landmark_dict = dict(zip(stations['station_id'].astype(int), stations['landmark'].str.lower().str.replace(' ', '_')))

trips['start_landmark'] = trips['start_terminal']
trips = trips.replace({'start_landmark':landmark_dict})

trips['end_landmark'] = trips['end_terminal']
trips = trips.replace({'end_landmark':landmark_dict})

print(trips.head())

#   add start hour column
trips['start_date'] = pd.to_datetime(trips['start_date'])
trips['start_hour'] = trips['start_date'].dt.hour

#   prune again!
# trips = trips[trips.loc[:,'start_landmark'] != trips.loc[:,'end_landmark']]

print(trips.head())

trips.groupby('start_landmark').boxplot(column='duration_minutes', by='start_hour')
# trips.groupby('start_landmark').plot(kind='line')
plt.title('Trip Duration by Start Hour')
plt.xlabel('Start Hour')
plt.ylabel('Duration in Minutes')
plt.show()




fig, ax = plt.subplots(figsize=(8,6))

for label, df in trips.groupby('start_landmark'):
    df.duration.plot(kind="line", ax=ax, label=label)
plt.legend()
# plt.title('Docks Available by Station ID in 2013')
# plt.xlabel('Date')
# plt.ylabel('Docks Available')

plt.show()


#   EOF
