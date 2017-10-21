import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#   Import stock data

#------------------------------------------------------------------------------
#   Load Data Sets
#------------------------------------------------------------------------------
print('Loading data...')

try:

    '''
        avoiding file_path_slug because the data is structured differently some files
    '''

    weather_path_01 = '../../../datasets/bayareabikeshare/201402_weather_data.csv'
    weather_01 = pd.read_csv(weather_path_01, header=0)

    weather_path_02 = '../../../datasets/bayareabikeshare/201408_weather_data.csv'
    weather_02 = pd.read_csv(weather_path_02, header=0)

    weather_path_03 = '../../../datasets/bayareabikeshare/201508_weather_data.csv'
    weather_03 = pd.read_csv(weather_path_03, header=0)

    weather_path_04 = '../../../datasets/bayareabikeshare/201608_weather_data.csv'
    weather_04 = pd.read_csv(weather_path_04, header=0)

    print('data loaded successfully!')
except:
    print('oops... something went wrong loading the data :(')


print('\n\n')


print('#' * 80)
#------------------------------------------------------------------------------
#   Data Prep
#------------------------------------------------------------------------------

print('Data cleanup started...')
# columns of weather_01 are named differently than the rest, set them to match
weather_01.columns = weather_02.columns

#   merge all dataframes into a giant weather frame
weather_frames = [weather_01, weather_02, weather_03, weather_04]
weather = pd.concat(weather_frames)

#   Trim down weather data to columns we care about, and name them better
columns_wanted =    ['PDT', 'Max TemperatureF', 'Mean TemperatureF', 'Min TemperatureF', ' Mean Wind SpeedMPH',  'PrecipitationIn', ' CloudCover', 'Zip']
column_new_names =  ['date', 'max_temp', 'mean_temp', 'min_temp', 'mean_wind', 'precipitation', 'cloud_cover', 'zip']

#   slim down dataframe to just things we need
weather = weather.loc[:,columns_wanted]
weather.columns = column_new_names

#   convert date column to datetime objects
weather['date'] = pd.to_datetime(weather['date'])

#   use date column as index
weather = weather.set_index('date')

#   precipitation column has a special 'T' value for trace amounts of rain, set all of these to zero
weather.loc[weather['precipitation'] == 'T', 'precipitation'] = 0.

#   force all columns to be numerical values
weather['precipitation'] = pd.to_numeric(weather['precipitation'], errors='coerce')

#   change zip to int
# df_weather['zip'] = df_weather['zip'].astype(int)

print('\tComplete!')


print('#' * 80)
#------------------------------------------------------------------------------
#   Statistical Analysis
#------------------------------------------------------------------------------

#look at unique values in each column
print('#' * 80)
print('#\tColumns and unique values')
# for col in column_new_names[1:]:
for col in weather.columns:
    print('Column : ' + col)
    print(pd.unique(weather[col]))
    print()

# print('#' * 80)
# print('#\tHEAD')
# print(df_weather.head())

print('#' * 80)
print('#\tINFO')
print(weather.info())

print('#' * 80)
print('#\tDESCRIBE')
print(weather.describe())

print('#' * 80)


#------------------------------------------------------------------------------
#   Data Visualization
#------------------------------------------------------------------------------

# # plot the min_temp and max_temp weather data as a scatter plot
# df_weather.groupby('zip').plot(kind='scatter', x='min_temp', y='max_temp')
# plt.xlabel='min_temp (F)'
# plt.ylabel='max_temp (F)'
# plt.show()


# #   plot mean_temp by zip
color_list = ['red', 'green', 'blue', 'orange', 'yellow']
counter = 0
fig, ax = plt.subplots(figsize=(8,6))
for label, df in weather.groupby('zip'):
    df.plot(kind='scatter', c=color_list[counter], x='min_temp', y='max_temp', ax=ax, label=label, alpha=0.3)
    counter += 1
plt.legend()
plt.title('Min vs Max Temperature')
plt.xlabel='min_temp (F)'
plt.ylabel='max_temp (F)'
plt.show()




# #   plot mean_temp by zip
fig, ax = plt.subplots(figsize=(8,6))
for label, df in weather.groupby('zip'):

    df_mean_temp = df['mean_temp']
    df_mean_temp = df_mean_temp.resample('W').mean()
    df_mean_temp.plot(kind="line", ax=ax, label=label)

plt.title('Mean Temperature by Date')
plt.xlabel='Date'
plt.ylabel='Mean Temperature (F)'
plt.legend()
plt.show()


#   EOF
