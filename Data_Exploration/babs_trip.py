

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

print('\n\n')
print('\n\n')

#------------------------------------------------------------------------------
#   Load Data Sets
#------------------------------------------------------------------------------
print('Loading data...')
try:

    file_path_slug = '../../../datasets/bayareabikeshare/201*_trip_data.csv'

    # glob all files
    file_list = glob(file_path_slug)

    trips = pd.DataFrame()

    counter = 1
    chunks = []
    for file in file_list:
        print('\nReading file [' + str(counter) + ' of ' + str(len(file_list)) + ']\t ' + str(file))

        # import file in chunks to temp DataFrame
        print('\treading chunks...')
        for chunk in pd.read_csv(file, chunksize=10000, iterator=True):

            chunk = chunk.set_index('Trip ID')

            # standardize column names
            chunk.columns = ['Duration', 'Start Date', 'Start Station', 'Start Terminal', 'End Date', 'End Station', 'End Terminal', 'Bike #', 'Subscriber Type', 'Zip Code']

            chunks.append(chunk)
            # print('0' * 80)
            # print(chunk.columns)


        print('\tfinished file!')
        counter += 1

    # status = pd.concat(chunks, ignore_index=True)
    trips = pd.concat(chunks)



    print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')

print('#' * 80)

#------------------------------------------------------------------------------
#   Data Cleanup - First Pass
#------------------------------------------------------------------------------
print('Data cleanup started...')

# station ID numbers that are in San Francisco
sf_stations = [ 39,41,42,45,46,47,48,49,50,51,54,55,56,57,58,59,60,61,62,63,
                64,65,66,67,68,69,70,71,72,73,74,75,76,77,82,90,91]


#   cleanup column names
print('cleaning up column names...')
new_cols = []
for col in trips.columns:
    new_col = col.replace(' ', '_').lower()
    new_cols.append(new_col)
trips.columns = new_cols

#   extract columns we want to keep
print('Subsetting to useful columns...')
important_cols = ['duration', 'start_date', 'start_terminal', 'end_date', 'end_terminal', 'bike_#', 'subscriber_type', 'zip_code']
trips = trips[important_cols]


print('\tfinished!')


#------------------------------------------------------------------------------
#   Prune Data
#------------------------------------------------------------------------------
print('Pruning Data...')
print('\timported Data set consists of %i entries' % len(trips.index))

#   prune data set by duration
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24


# subset trips by duration
print('\tpruning data to trips more than 10 minutes long...')
ten_min_plus_trips = trips[trips['duration'] > 10 * minute].copy()
print('\t\tpruned data set \'ten_min_plus_trips\' consists of %i entries' % len(ten_min_plus_trips.index))

print('\tpruning data to trips no more than 10 minutes long...')
ten_min_less_trips = trips[trips['duration'] <= 10 * minute].copy()
print('\t\tpruned data set \'ten_min_less_trips\' consists of %i entries' % len(ten_min_less_trips.index))

print('\tfinished!')





#------------------------------------------------------------------------------
#   Statistical Analysis
#------------------------------------------------------------------------------

def printDataDistribution(dataSet, category, spread_list):
    print('#' * 60)
    print('Data Distributin by \'%s\'' % category)

    for interval in spread_list:
        tempDF = dataSet[dataSet[category] <= interval]
        tempDF_ratio = float(len(tempDF.index)) / float(len(dataSet.index)) * 100.0
        print('Data Spread:\t%s\t%.2f\t%i' % (interval, tempDF_ratio, len(tempDF.index)))
    print('#' * 60)

# print interval spread of duration in minutes
intervals = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60]
intervals_minutes = [60 * i for i in intervals]
printDataDistribution(trips, 'duration', intervals_minutes)

# # look at unique values in each column
# print('#' * 80)
# print('#\tColumns and unique values')
# detail_cols = ['start_date']
# detail_cols = ['start_terminal', 'end_terminal', 'bike_#', 'subscriber_type', 'subscription_type', 'zip_code']
# for col in detail_cols:
#     print('Column : ' + col + '\t' + str(len(pd.unique(trips[col]))))
#     print(pd.unique(trips[col]))
#     print()

# print('#' * 80)
# print('#\tHEAD')
# print(trips.head())
#
# print('#' * 80)
# print('#\tTail')
# print(trips.tail())
#
print('#' * 80)
print('#\tINFO')
print(trips.info())
#
# print('#' * 80)
# print('#\tDESCRIBE')
# print(trips.describe())
#
#
# #------------------------------------------------------------------------------
# #   Data Cleanup - Second Pass
# #------------------------------------------------------------------------------
# print('Data cleanup started...')
#
# #   create duration_minutes column
# trips['duration_minutes'] = trips['duration'] / 60.
#
# #   convert end and start dates to datetime objects
# print('\tconverting end and start dates to datetime objects...')
# trips['start_date'] = pd.to_datetime(trips['start_date'], format="%m/%d/%Y %H:%M")
# trips['end_date'] = pd.to_datetime(trips['end_date'], format="%m/%d/%Y %H:%M")
# print('\t\tfinished!')
# #   create pickup hour column
# trips['start_hour'] = trips['start_date'].dt.hour
#
#
#
# #------------------------------------------------------------------------------
# #   one way trips
# #------------------------------------------------------------------------------
# #   subset trips that leave and return to same terminal
# print('\tpruning data to one way trips...')
# # round_trips = trips.loc[trips['start_terminal'] == trips['end_terminal']]
# round_trips = trips.loc[trips.loc[:,'start_terminal'] == trips.loc[:,'end_terminal']].copy()
# print('\t\tpruned data set now consists of %i lines' % len(round_trips.index))
#
#
#
# #   convert end and start dates to datetime objects
# print('\tconverting end and start dates to datetime (round_trips)  objects...')
# round_trips.loc[:,'start_date'] = pd.to_datetime(round_trips.loc[:,'start_date'], format="%m/%d/%Y %H:%M")
# round_trips.loc[:,'end_date'] = pd.to_datetime(round_trips.loc[:,'end_date'], format="%m/%d/%Y %H:%M")
# print('\t\tfinished!')
# #   create pickup hour column
# round_trips.loc[:,'start_hour'] = round_trips.loc[:,'start_date'].dt.hour
#
# #------------------------------------------------------------------------------
# #   round trips
# #------------------------------------------------------------------------------
# #   subset trips that leave and return to same terminal
# print('\tpruning data to round trips...')
# one_way_trips = trips.loc[trips['start_terminal'] != trips['end_terminal']].copy()
# print('\t\tpruned data set now consists of %i lines' % len(one_way_trips.index))
#
# #   convert end and start dates to datetime objects
# print('\tconverting end and start dates to datetime objects (one_way_trips) ...')
# one_way_trips['start_date'] = pd.to_datetime(one_way_trips['start_date'], format="%m/%d/%Y %H:%M")
# # one_way_trips['end_date'] = pd.to_datetime(one_way_trips['end_date'], format="%m/%d/%Y %H:%M")
# print('\t\tfinished!')
# #   create pickup hour column
# one_way_trips['start_hour'] = one_way_trips['start_date'].dt.hour





# #------------------------------------------------------------------------------
# #   Data Visualization
# #------------------------------------------------------------------------------
#
#
# #   plot ride duration
#
# round_trips.plot(kind='scatter', x='start_hour', y='duration_minutes')
# plt.title('Trip Duration by Start Hour')
# plt.xlabel='Start Hour'
# plt.ylabel='Duration in Minutes'
# plt.show()
# #
# # one_way_trips.plot(kind='scatter', x='start_hour', y='duration_minutes')
# # plt.title('Trip Duration by Start Hour')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Duration in Minutes'
# # plt.show()
#
#
# # # plot trip duration by start hour
# # trips.boxplot(column='duration_minutes', by='start_hour')
# # plt.title('Trip Duration by Start Hour')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Duration in Minutes'
# # plt.show()
#
# # # plot start vs end terminal
# # trips.plot(kind='scatter', x='start_terminal', y='end_terminal')
# # plt.title('Starting Terminal to End Terminal')
# # plt.xlabel='Start Terminal'
# # plt.ylabel='End Terminal'
# # plt.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
# # # plot histogram of trip duration
# # ax = trips['duration_minutes'].plot(kind='hist', color='r', alpha=0.25, bins=200, figsize=(20,5))
# # round_trips['duration_minutes'].plot(kind='hist', color='g', alpha=0.25, bins=200, ax=ax)
# # one_way_trips['duration_minutes'].plot(kind='hist', color='b', alpha=0.25, bins=200, ax=ax)
# # plt.title('Spread of One Way Trips Duration by length in Minutes')
# # plt.xlabel='Trip Duration (Minutes)'
# # plt.ylabel='Number of Trips'
# # plt.legend(['trips','round_trips', 'one_way_trips'],loc='best')
# # plt.show()
#
#
#
#
#
#
# # # plot count of one way trips by start_terminal
# # ax = one_way_trips.groupby(['start_terminal']).size().plot(kind='bar', color = 'r', position=0, figsize=(20, 5))
# # # plt.title('Number of One Way Trips starting from each Terminal')
# # # plt.show()
# #
# # # plot count of one way trips by end_terminal
# # one_way_trips.groupby(['end_terminal']).size().plot(kind='bar', color = 'b', position=1, ax=ax)
# # # plt.title('Number of One Way Trips ending at each Terminal')
# # plt.title('Number of One Way Trips by Terminal')
# # plt.show()
#
# # # plot count of one way trips by start_terminal
# # # ax = trips.groupby(['start_terminal'])['duration_minutes'].mean().plot(kind='bar', color = 'r', position=0, figsize=(20, 4))
# # ax = round_trips.groupby(['start_terminal'])['duration_minutes'].mean().plot(kind='bar', color = 'g', position=0, figsize=(20, 5), legend=True)
# # one_way_trips.groupby(['start_terminal'])['duration_minutes'].mean().plot(kind='bar', color = 'b', position=1, figsize=(20, 5), legend=True, ax=ax)
# # plt.title('Mean Duration by Terminal')
# # plt.xlabel='Terminal ID'
# # plt.ylabel='Mean Duration (minutes)'
# # plt.legend(['round_trips', 'one_way_trips'],loc='best')
# # plt.show()
#
# # plot trip duration by start hour
# ax = trips.groupby(['start_hour'])['duration_minutes'].count().plot(kind='bar', color='b', position=0, figsize=(20,5))
# trips.groupby(['start_hour'])['duration_minutes'].sum().plot(kind='bar', color='g', position=1, figsize=(20,5), ax=ax)
# plt.title('Trip Duration by Start Hour')
# plt.xlabel='Start Hour'
# plt.legend(['Count', 'Sum'], loc='best')
# plt.show()
#
#
# # plot trip duration by start hour
# ax = one_way_trips.groupby(['start_hour'])['duration_minutes'].count().plot(kind='bar', color='b', position=0, figsize=(20,5))
# one_way_trips.groupby(['start_hour'])['duration_minutes'].sum().plot(kind='bar', color='g', position=1, figsize=(20,5), ax=ax)
# plt.title('Trip Duration by Start Hour (one way)')
# plt.xlabel='Start Hour'
# plt.legend(['Count', 'Sum'], loc='best')
# plt.show()
#
#
# # plot trip duration by start hour
# ax = round_trips.groupby(['start_hour'])['duration_minutes'].count().plot(kind='bar', color='b', position=0, figsize=(20,5))
# round_trips.groupby(['start_hour'])['duration_minutes'].sum().plot(kind='bar', color='g', position=1, figsize=(20,5), ax=ax)
# plt.title('Trip Duration by Start Hour (round trip)')
# plt.xlabel='Start Hour'
# plt.legend(['Count', 'Sum'], loc='best')
# plt.show()
#
# # plot count of departures from each start terminal
# ax = trips.groupby(['start_terminal'])['duration_minutes'].count().plot(kind='bar', alpha=0.4, color='g', figsize=(10,5))
# trips.groupby(['end_terminal'])['duration_minutes'].count().plot(kind='bar', alpha=0.4, color='b', figsize=(10,5), ax=ax)
# plt.title('Number of departers from each terminal')
# plt.xlabel='Terminal Number'
# plt.ylabel='Number of Departures'
# plt.legend(['Start Term','End Term'],loc='best')
# plt.show()
#
#
#
#
#
#
# #------------------------------------------------------------------------------
# #       Prune to trips that start at SF stations
# #------------------------------------------------------------------------------
#
#
# only_sf_trips = trips.loc[trips['start_terminal'].isin(sf_stations)].copy()
# non_sf_trips = trips.loc[~trips['start_terminal'].isin(sf_stations)].copy()
#
# # plot count of departures from each start terminal
# ax = only_sf_trips.groupby(['start_terminal'])['duration_minutes'].count().plot(kind='bar', alpha=0.4, color='g', figsize=(10,5))
# only_sf_trips.groupby(['end_terminal'])['duration_minutes'].count().plot(kind='bar', alpha=0.4, color='b', figsize=(10,5), ax=ax)
# plt.title('Number of departers from each terminal (SF only)')
# plt.xlabel='Terminal Number'
# plt.ylabel='Number of Departures'
# plt.legend(['Start Term','End Term'],loc='best')
# plt.show()
#
#
# # plot count of departures from each start terminal
# ax = non_sf_trips.groupby(['start_terminal'])['duration_minutes'].count().plot(kind='bar', alpha=0.4, color='g', figsize=(10,5))
# non_sf_trips.groupby(['end_terminal'])['duration_minutes'].count().plot(kind='bar', alpha=0.4, color='b', figsize=(10,5), ax=ax)
# plt.title('Number of departers from each terminal (Non SF only)')
# plt.xlabel='Terminal Number'
# plt.ylabel='Number of Departures'
# plt.legend(['Start Term','End Term'],loc='best')
# plt.show()
#
#
#
#
#
#
# # plot count of departures from each start terminal
# sf_trip_start_term = only_sf_trips.groupby(['start_terminal'])['duration'].count()
# sf_trip_end_term   = only_sf_trips.groupby(['end_terminal'])['duration'].count()
# (sf_trip_end_term - sf_trip_start_term).plot(kind='bar', color='r')
# plt.title('Influx of bikes to each station (incoming - outgoing)')
# plt.xlabel='Terminal Number'
# plt.ylabel='Bike Influx'
# # plt.legend(['SF', 'Non SF'],loc='best')
# plt.show()
#
#
# non_sf_trip_start_term = non_sf_trips.groupby(['start_terminal'])['duration'].count()
# non_sf_trip_end_term   = non_sf_trips.groupby(['end_terminal'])['duration'].count()
# (non_sf_trip_end_term - non_sf_trip_start_term).plot(kind='bar', color='b')
# plt.title('Influx of bikes to each station (incoming - outgoing)')
# plt.xlabel='Terminal Number'
# plt.ylabel='Bike Influx'
# # plt.legend(['SF', 'Non SF'],loc='best')
# plt.show()
#
#
# # # plot trip duration by start hour
# # one_way_trips.groupby(['start_hour'])['duration_minutes'].mean().plot(kind='bar', figsize=(20,5))
# # plt.title('Mean One Way Trip Duration by Start Hour (one way trips)')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Mean Duration (minutes)'
# # plt.show()
# #
# #
# # # plot trip duration by start hour
# # one_way_trips.groupby(['start_hour'])['duration_minutes'].count().plot(kind='bar', figsize=(20,5))
# # plt.title('Count One Way Trip Duration by Start Hour (one way trips)')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Sum Duration (minutes)'
# # plt.show()
# #
# #
# #
# # # plot trip duration by start hour
# # trips.groupby(['start_hour'])['duration_minutes'].mean().plot(kind='bar', figsize=(20,5))
# # plt.title('Mean Trip Duration by Start Hour')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Mean Duration (minutes)'
# # plt.show()
# #
# #
# # # plot trip duration by start hour
# # trips.groupby(['start_hour'])['duration_minutes'].count().plot(kind='bar', figsize=(20,5))
# # plt.title('Count Trip Duration by Start Hour (one way trips)')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Sum Duration (minutes)'
# # plt.show()
# #
# #
# # # plot trip duration by start hour
# # round_trips.groupby(['start_hour'])['duration_minutes'].mean().plot(kind='bar', figsize=(20,5))
# # plt.title('Mean Round Trip Duration by Start Hour (round trips)')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Mean Duration (minutes)'
# # plt.show()
# #
# # # plot trip duration by start hour
# # round_trips.groupby(['start_hour'])['duration_minutes'].count().plot(kind='bar', figsize=(20,5))
# # plt.title('Count Round Trip Duration by Start Hour')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Sum Duration (minutes)'
# # plt.show()
# #
# # # plot trip duration by start hour
# # round_trips.groupby(['start_hour'])['duration_minutes'].sum().plot(kind='bar', figsize=(20,5))
# # plt.title('Sum Round Trip Duration by Start Hour')
# # plt.xlabel='Start Hour'
# # plt.ylabel='Sum Duration (minutes)'
# # plt.show()
#
#
# # Split ride frequency by commuter type
#
#
#
# '''
# 7869184
#  955557
# '''
#
#
# #   EOF
