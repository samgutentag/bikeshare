# Generate 'Time Machine' of Trip Route Heatmaps, minute by minute


# Imports
import matplotlib
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import datetime

import seaborn as sns
sns.set_style('whitegrid')
sns.set_context("poster")

# Usafull Global Settings
font = {'size'   : 50}
matplotlib.rc('font', **font)

TITLE_FONT_SIZE = 25
LABEL_FONT_SIZE = 15

GRID_DIMS = 15

#----------------------------------------------------------------------------------------------------------------
# Load Morning Commute Trip Data
#----------------------------------------------------------------------------------------------------------------
print('[%s] Loading Morning Commute Trips Data...' % datetime.datetime.now().time())

morning_commutes = pd.DataFrame()
trip_data_file = '../clean_data/bayareabikeshare/trip_data_morning_commutes.csv'

# Chunk Settings
chunks = []
chunk_counter = 1
chunksize = 10000
# num_chunks = math.ceil(sum(1 for row in open(trip_data_file, 'r'))/chunksize)

# import file in chunks
for chunk in pd.read_csv(trip_data_file, chunksize=chunksize, iterator=True, index_col=0, parse_dates=['start_date', 'end_date', 'forecast_time']):

    # append chunk to chunks list
    chunks.append(chunk)

    # if chunk_counter == 1 or chunk_counter % math.ceil(num_chunks/10) == 0 or chunk_counter == num_chunks:
    #     print('\t\t[%s] finished chunk %s of %s' % (datetime.datetime.now().time(), chunk_counter, num_chunks))
    # chunk_counter += 1

morning_commutes = pd.concat(chunks)
morning_commutes.user_type = morning_commutes.user_type.astype('category')
print('[%s] Complete!' % datetime.datetime.now().time())

#----------------------------------------------------------------------------------------------------------------
# Load Evening Commute Trip Data
#----------------------------------------------------------------------------------------------------------------
print('[%s] Loading Evening Commute Trips Data...' % datetime.datetime.now().time())

evening_commutes = pd.DataFrame()
trip_data_file = '../clean_data/bayareabikeshare/trip_data_evening_commutes.csv'

# Chunk Settings
chunks = []
chunk_counter = 1
chunksize = 10000
# num_chunks = math.ceil(sum(1 for row in open(trip_data_file, 'r'))/chunksize)

# import file in chunks
for chunk in pd.read_csv(trip_data_file, chunksize=chunksize, iterator=True, index_col=0, parse_dates=['start_date', 'end_date', 'forecast_time']):

    # append chunk to chunks list
    chunks.append(chunk)

    # if chunk_counter == 1 or chunk_counter % math.ceil(num_chunks/10) == 0 or chunk_counter == num_chunks:
    #     print('\t\t[%s] finished chunk %s of %s' % (datetime.datetime.now().time(), chunk_counter, num_chunks))
    # chunk_counter += 1

evening_commutes = pd.concat(chunks)
evening_commutes.user_type = evening_commutes.user_type.astype('category')
print('[%s] Complete!' % datetime.datetime.now().time())


#----------------------------------------------------------------------------------------------------------------
# Load Customer and Subscriber Trip Data
#----------------------------------------------------------------------------------------------------------------
print('[%s] Loading Customer and Subscriber Trips Data...' % datetime.datetime.now().time())
file_path_slug = '../clean_data/bayareabikeshare/trip_data_extended_cleaned_20*.csv'
file_list = glob(file_path_slug)

all_trips = pd.DataFrame()

counter = 1
chunks = []

for file in file_list:

    # num_chunks = math.ceil(sum(1 for row in open(file, 'r'))/10000)

    # chunk_counter = 1
    for chunk in pd.read_csv(file, chunksize=10000, index_col=0, iterator=True, parse_dates=['start_date', 'end_date']):
        # prune out non Customer trips and non San Francisco trips
        chunk = chunk[(chunk.start_station_region == 'San Francisco') &
                      (chunk.end_station_region == 'San Francisco')].copy()
        # append chunk to chunks list
        chunks.append(chunk)

        # if chunk_counter == 1 or chunk_counter % math.floor(num_chunks/2) == 0 or chunk_counter == num_chunks:
        #     print('\t[%s] finished chunk %s of %s' % (datetime.datetime.now().time(), chunk_counter, num_chunks))
        # chunk_counter += 1

    print('\tFinished file! (%d of %d)' % (counter, len(file_list)))
    counter += 1

all_trips = pd.concat(chunks)

# Split into subscriber and commuter frames
customer_trips   = all_trips[all_trips.user_type == 'Customer'].copy()
customer_trips.reset_index(inplace=True, drop=True)
subscriber_trips = all_trips[all_trips.user_type == 'Subscriber'].copy()
subscriber_trips.reset_index(inplace=True, drop=True)


all_trips = pd.DataFrame()

print('[%s] Complete!' % datetime.datetime.now().time())



#----------------------------------------------------------------------------------------------------------------
# Load Station Data
#----------------------------------------------------------------------------------------------------------------
print('[%s] Loading Station Data...' % datetime.datetime.now().time())
stations = pd.read_csv('../clean_data/bayareabikeshare/station_data_cleaned.csv',
                       index_col=0, parse_dates=['first_service_date', 'last_service_date'])

stations = stations[stations.region == 'San Francisco'].copy()
stations.reset_index(inplace=True, drop=True)

# station 73 was expanded, we dont care about that right now, we just want days open.
# copy last_service_date from second entry to first, need total days
stations.iloc[29,7] = stations.iloc[30,7]
# add days in sevice to second entry to first entry
stations.iloc[29,9] += stations.iloc[30,9]
# drop second entry
stations.drop_duplicates(subset=['station_id'], inplace=True)

stations.reset_index(inplace=True, drop=True)
# stations.head()
print('[%s] Complete!' % datetime.datetime.now().time())

#----------------------------------------------------------------------------------------------------------------
# Plotting Functions
#----------------------------------------------------------------------------------------------------------------
def make_route_grid(trip_df=None, station_ids=stations.station_id):
    index   = [x for x in station_ids]
    columns = [x for x in station_ids]

    trip_grid = pd.DataFrame(index=index, columns=columns)

    # create grid of trips from start to end terminal counts
    for sid in station_ids:
        for eid in station_ids:
            # count trips between terminals
            route_count = trip_df[(trip_df.start_station_id == sid) & (trip_df.end_station_id == eid)].shape[0]
            trip_grid.loc[eid, sid] = route_count

    trip_grid = trip_grid.iloc[::-1]
    return trip_grid

def make_outbound_grid(trip_df=None, station_ids=stations.station_id):
    index   = [x for x in station_ids]
    columns = [x for x in station_ids]

    trip_grid = pd.DataFrame(index=index, columns=columns)
    # morning_trip_grid

    # create grid of trips from start to end terminal counts
    for sid in station_ids:
        route_count = trip_df[(trip_df.start_station_id == sid)].shape[0]
        trip_grid.loc[eid, sid] = route_count

    trip_grid = trip_grid.iloc[::-1]
    return trip_grid

def make_inbound_grid(trip_df=None, station_ids=stations.station_id):
    index   = [x for x in station_ids]
    columns = [x for x in station_ids]

    trip_grid = pd.DataFrame(index=index, columns=columns)
    # morning_trip_grid

    # create grid of trips from start to end terminal counts
    for eid in station_ids:
        # count trips between terminals
        route_count = trip_df[(trip_df.end_station_id == eid)].shape[0]
        trip_grid.loc[eid, sid] = route_count

    trip_grid = trip_grid.iloc[::-1]
    return trip_grid

def timeline_grid_plots(df=morning_commutes, prefix='Morning Commuter'):

    print('[%s] Starting %s Grids...' % (datetime.datetime.now().time(), prefix))

    trip_grids = list()
    datetime_stamps = list()
    file_count = len(sorted(df.start_date.dt.date.unique()))

    cumm_grid = pd.DataFrame()

    for i, date in enumerate(sorted(df.start_date.dt.date.unique())):
        date_trips = df[df.start_date.dt.date == date].copy()

        trip_grid = make_route_grid(trip_df=date_trips)
        if cumm_grid.shape[0] == 0:
            cumm_grid = trip_grid.copy()
        else:
            cumm_grid += trip_grid



        print('trip_grid {}'.format(str(trip_grid.sum().sum())))
        print('cumm_grid {}'.format(str(cumm_grid.sum().sum())))


        print('\t../charts/station_trends/time_machine/%s/%s_route_heatmap_%s.png of %s' % (prefix.replace(' ','_').lower(),
                                                                                            prefix.replace(' ','_').lower(),
                                                                                            str(i).zfill(10),
                                                                                            file_count))

        mask = cumm_grid == 0
        fig, ax = plt.subplots(figsize=(GRID_DIMS*1.5, GRID_DIMS))

        cmap = sns.color_palette('OrRd', 20)

        if prefix.lower() == 'subscriber':
            cmap = sns.color_palette('Blues', 20)

        if prefix.lower() == 'customer':
            cmap = sns.color_palette('Reds', 20)

        if prefix.lower() == 'commuter':
            cmap = sns.color_palette('Greens', 20)

        sns.heatmap(data=cumm_grid, linecolor='grey', linewidths=.5, square=True, cmap=cmap,
                    mask=mask, ax=ax, cbar_kws={"shrink": .75}, cbar=True)

        ax.set_xlabel('Start Station', size=LABEL_FONT_SIZE, weight='bold')
        ax.set_ylabel('End Station', size=LABEL_FONT_SIZE, weight='bold')

        title = '%s Route Heatmap - %s' % (prefix, str(date).replace('T', ' ').split('.')[0])
        ax.set_title(title, size=TITLE_FONT_SIZE, weight='bold')

        plt.savefig('../charts/station_trends/time_machine/%s/%s_route_heatmap_%s.png' % (prefix.replace(' ','_').lower(), prefix.replace(' ','_').lower(), str(i).zfill(10)))
        plt.close()



    print('[%s] Plots Complete!' % datetime.datetime.now().time())



#----------------------------------------------------------------------------------------------------------------
# Make Time Machine Plots!
#----------------------------------------------------------------------------------------------------------------

commuter_trips = pd.concat([morning_commutes, evening_commutes])
commuter_trips.drop_duplicates(subset=['trip_id'], inplace=True)
commuter_trips.reset_index(inplace=True, drop=True)


print('%s Total Subscriber Trips' % str(subscriber_trips.shape[0]).ljust(8))
print('%s Total Customer Trips' % str(customer_trips.shape[0]).ljust(8))
print('%s Total Commuter Trips' % str(commuter_trips.shape[0]).ljust(8))



timeline_grid_plots(df=commuter_trips, prefix='Commuter')
timeline_grid_plots(df=customer_trips, prefix='Customer')
timeline_grid_plots(df=subscriber_trips, prefix='Subscriber')


# EOF
