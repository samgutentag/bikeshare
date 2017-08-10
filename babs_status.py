

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

    file_path_slug = '../../datasets/bayareabikeshare/2016*_status_data.csv'

    # glob all files
    file_list = glob(file_path_slug)

    status = pd.DataFrame()

    counter = 1
    chunks = []
    for file in file_list:
        print('\nReading file [' + str(counter) + ' of ' + str(len(file_list)) + ']\t ' + str(file))

        # import file in chunks to temp DataFrame
        print('\treading chunks...')
        # 16994602
        for chunk in pd.read_csv(file, chunksize=10000, iterator=True, parse_dates=['time'], index_col=False):

            # set time to index of chunk
            chunk = chunk.set_index('time')

            chunks.append(chunk)

        print('finished file!')
        counter += 1


    # status = pd.concat(chunks, ignore_index=True)
    status = pd.concat(chunks)
    # print(status.head())


    print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')


print('\n\n')


print('#' * 80)
#------------------------------------------------------------------------------
#   Data Prep
#------------------------------------------------------------------------------

print('Data cleanup started...')

#   convert time to datetime
# print('\tconverting time to datetype type')
# status['time'] = pd.to_datetime(status['time'])


print('\n\nstatus')
print(status.info())
print(status.describe())


#   use time column as index
# print('\tsetting time column as index')
# status = status.set_index('time')

print('\tComplete!')
print('#' * 80)

# #------------------------------------------------------------------------------
# #   Statistical Analysis
# #------------------------------------------------------------------------------
#
# # #   look at unique values in each column
# # print('#' * 80)
# # print('#\tColumns and unique values')
# # for col in important_cols:
# #     print('Column : ' + col + '\t' + str(len(pd.unique(status[col]))))
# #     print(pd.unique(status[col]))
# #     print()
# #
# print('#\tHEAD')
# print(status.head())
# print('#' * 80)
#
# print('#\tTAIL')
# print(status.tail())
# print('#' * 80)
#
# print('#\tINFO')
# print(status.info())
# print('#' * 80)
#
# # print('#\tDESCRIBE')
# # print(status.describe())
# # print('#' * 80)
#
#
# #------------------------------------------------------------------------------
# #   Split Up by Areas
# #------------------------------------------------------------------------------
#
#
#
#
#
# #------------------------------------------------------------------------------
# #   Data Visualization
# #------------------------------------------------------------------------------
#
# # status['bikes_available'].plot(legend=True)
# # # plt.title('Temperature over time')
# # plt.ylabel= 'bikes_available'
# # plt.show()
#
#
#
#
#


# status_docks_available = status['docks_available']['2014']
#
# # Resample to daily data, aggregating by max: daily_highs
# status_docks_available_weekly_mean = status_docks_available.resample('W').mean()
#
# # Use a rolling 7-day window with method chaining to smooth the daily high temperatures in August
# status_docks_available_weekly_mean_smoothed = status_docks_available_weekly_mean.rolling(window=4).mean()
#
# status_docks_available_weekly_mean_smoothed.plot()
# plt.title('Docks Available by Date, Rolling Weekly Mean')
# plt.xlabel('Date')
# plt.ylabel('Docks Available')
# plt.show()







# fig, ax = plt.subplots(figsize=(8,6))
#
# # for key in status.columns:
# #     print('?' + str(key) + '?' )
#
#
# # status_resample = status['2013-09':'2013-10']
# print(status.info())
# print(status.head())
# print(status.tail())
#
# for label, df in status.groupby('station_id'):
#     df.docks_available.plot(kind="kde", ax=ax, label=label)
# plt.legend()
# plt.title('Docks Available by Station ID in 2013')
# plt.xlabel('Date')
# plt.ylabel('Docks Available')
#
# plt.show()







#
#
# #   EOF
