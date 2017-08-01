

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

    file_path_slug = '../../datasets/bayareabikeshare/2014*_trip_data.csv'

    # glob all files
    file_list = glob(file_path_slug)

    status = pd.DataFrame()

    counter = 1
    chunks = []
    for file in file_list:
        print('\nReading file [' + str(counter) + ' of ' + str(len(file_list)) + ']\t ' + str(file))

        # import file in chunks to temp DataFrame
        print('\treading chunks...')
        for chunk in pd.read_csv(file, chunksize=10000, iterator=True):

            chunk = chunk.set_index('Trip ID')

            chunks.append(chunk)

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

#   prune data set by duration
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24

# subset trips that are less than one hour in duration
trips = trips[trips['duration'] < hour]

#   subset trips that leave and return to same terminal
trips = trips[trips.loc[:,'start_terminal'] == trips.loc[:,'end_terminal']]
print('\tfinished!')

#------------------------------------------------------------------------------
#   Data Cleanup - Second Pass
#------------------------------------------------------------------------------
print('Data cleanup started...')

#   create duration_minutes column
trips['duration_minutes'] = trips['duration'] / 60.

#   convert end and start dates to datetime objects
print('converting end and start dates to datetime objects...')
trips['start_date'] = pd.to_datetime(trips['start_date'])
# trips['end_date'] = pd.to_datetime(trips['end_date'])
print('\tfinished!')


#   create pickup hour column
trips['start_hour'] = trips['start_date'].dt.hour

print(trips.describe())


#------------------------------------------------------------------------------
#   Statistical Analysis
#------------------------------------------------------------------------------




# look at unique values in each column
print('#' * 80)
print('#\tColumns and unique values')
detail_cols = ['duration', 'start_terminal', 'end_terminal', 'subscriber_type', 'zip_code']
for col in detail_cols:
    print('Column : ' + col + '\t' + str(len(pd.unique(trips[col]))))
    print(pd.unique(trips[col]))
    print()

print('#' * 80)
print('#\tHEAD')
print(trips.head())

print('#' * 80)
print('#\tTail')
print(trips.tail())

# print('#' * 80)
# print('#\tINFO')
# print(trips.info())

# print('#' * 80)
# print('#\tDESCRIBE')
# print(trips.describe())



#------------------------------------------------------------------------------
#   Data Visualization
#------------------------------------------------------------------------------


#   plot ride duration

# trips.plot(kind='scatter', x='start_hour', y='duration_minutes')
# plt.title('Trip Duration by Start Hour')
# plt.xlabel('Start Hour')
# plt.ylabel('Duration in Minutes')
# plt.show()


# trips.boxplot(column='duration_minutes', by='start_hour')
# plt.title('Trip Duration by Start Hour')
# plt.xlabel('Start Hour')
# plt.ylabel('Duration in Minutes')
# plt.show()


# trips.plot(kind='scatter', x='start_terminal', y='end_terminal')
# plt.title('Starting Terminal to End Terminal')
# plt.xlabel('Start Terminal')
# plt.ylabel('End Terminal')
# plt.show()


# plot subsciber vs customer usage by hour




#   EOF
