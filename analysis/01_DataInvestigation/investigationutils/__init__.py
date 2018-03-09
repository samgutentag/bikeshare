

import datetime
import numpy as np
import pandas as pd
from glob import glob
from math import ceil

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns


LABEL_FONT_SIZE = 15
TITLE_FONT_SIZE = 25
TICK_FONT_SIZE = LABEL_FONT_SIZE*0.8
FIG_SIZE = (15,6)

day_labels = ['MON','TUE','WED','THU','FRI','SAT','SUN']
day_labels_full = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']
month_labels = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

sub_color = 'b'
sub_color_alt = 'm'
cust_color='r'
cust_color_alt='y'

commuter_color='g'
commuter_color_alt='#1daf1d'

commuter_am = '#ea54d9'
commuter_am_alt = '#9b8460'

commuter_pm = '#b97ccc'
commuter_pm_alt = '#f4ad3a'

fade_alpha=0.25
significant_dates = {}


def csv_chunk_importer(file_path_slug='', column_labels=[], chunk_size=10000, drop_dups=False):
    """Load a collection of files in chunks

    Parameters
    ----------
    file_path_slug : string (required)
        file path to be searched, case use wildcards or single files

    column_labels : list (optional)
        a list of column names to replace the columns derived from the csv file
        will not rename columns if column counts do not match

    chunk_size : int (optional)
        the line size of each chunk being loaded
        defaults to 10000

    drop_dups : bool (optional)
        drop duplicate rows
        defaults to False


    Returns
    ----------
    df : pandas.DataFrame
        a data frame object of the loaded csv data

    """



    time_marker('Started Loading Data...')
    file_list = glob(file_path_slug)

    file_count = len(file_list)

    df = pd.DataFrame()

    # counter = 1
    chunks = []

    for ii, file in enumerate(file_list):

        for chunk in pd.read_csv(file, chunksize=10000, iterator=True):

            if len(column_labels) == len(chunk.columns):
                chunk.columns = column_labels

            chunks.append(chunk)

        if file_count < 50:
            time_marker('\tFinished file! ({:d} of {:d})'.format(ii+1, len(file_list)))
        elif file_count >= 50 and file_count < 1000:
            if ii % 100 == 0 or ii == 0 or ii == file_count:
                time_marker('\tFinished file! ({:d} of {:d})'.format(ii+1, len(file_list)))
        else:
            if ii % 1000 == 0 or ii == 0 or ii == file_count:
                time_marker('\tFinished file! ({:d} of {:d})'.format(ii+1, len(file_list)))

    time_marker('concatenating chunks...')
    df = pd.concat(chunks)

    if drop_dups:
        df.drop_duplicates(inplace=True)

    df.reset_index(inplace=True, drop=True)
    time_marker('Data Loaded Successfully!')

    return df

def time_marker(text=''):
    """Pretty print a time stamp with string

    Parameters
    ----------
    text : string (optional)
        string to be printed

    Returns
    ----------
    DOES NOT RETURN

    """
    print('[{}] {}'.format(datetime.datetime.now().time(), text.strip()))

def plot_hourly_trips(df, chart_title='San Francisco Subscriber Hourly Trip Count',
                        file_name='../../charts/hourly_subscriber_trip.png', user_group='subs',
                        y_scale=10000, DO_WRITE_CHARTS=False):

    hourly_starting = df.groupby([df.start_date.dt.hour]).count()
    hourly_ending = df.groupby([df.end_date.dt.hour]).count()

    starting_x_ticks = sorted(hourly_starting.index.unique())
    ending_x_ticks = sorted(hourly_ending.index.unique())

    if user_group == 'subs':
        main_color = sub_color
        alt_color = sub_color_alt
    else:
        main_color = cust_color
        alt_color = cust_color_alt

    plt.subplots(figsize=FIG_SIZE)
    ax = sns.barplot(x = starting_x_ticks , y = 'trip_id', data=hourly_starting, color=main_color, alpha = 0.35, label='Trips Starting')
    sns.barplot(ax=ax, x = ending_x_ticks , y = 'trip_id', data=hourly_ending, color=alt_color, alpha = 0.35, label='Trips Ending')

    ax.set_title(chart_title, size=TITLE_FONT_SIZE)

    ax.set_xlabel('Hour of Day', size=LABEL_FONT_SIZE)
    ax.set_ylabel('Trip Count', size=LABEL_FONT_SIZE)
    ax.legend(loc=1, frameon=True)

    y_max = hourly_starting.trip_id.max()

    if hourly_ending.trip_id.max() > y_max:
        y_max = hourly_ending.trip_id.max()

    y_max = ceil(y_max/y_scale)*y_scale

    y_ticks = [x for x in range(0, y_max+y_scale, y_scale)]
    for y in y_ticks:
        ax.axhline(y, linestyle=':', color='k', alpha=0.15)

    ax.grid(False)


    if DO_WRITE_CHARTS:
        plt.savefig(file_name)
    plt.show()
    plt.close()

def plot_weekly_trips(df, chart_title='San Francisco Subscriber Weekly Trip Counts',
                      file_name='../../charts/weekly_subscriber_trip.png', user_group='subs',
                      y_scale=1000, DO_WRITE_CHARTS=False):

    if user_group == 'subs':
        main_color = sub_color
    else:
        main_color = cust_color

    tmp = df.copy()
    tmp = tmp.groupby([tmp.start_date]).count()['trip_id'].to_frame()
    tmp = tmp.resample('1Min').sum()
    tmp.fillna(0, inplace=True)
    weekly_trips = tmp.groupby([tmp.index.dayofweek, tmp.index.hour]).sum()

    x_tick_labels = day_labels_full
    x_ticks = [x*24+12 for x in range(0, len(x_tick_labels))]

    x_markers = [x*24 for x in range(1, len(x_tick_labels))]

    plt.subplots(figsize=FIG_SIZE)
    ax = sns.barplot(x = weekly_trips.index , y = 'trip_id', data=weekly_trips, color=main_color, alpha = 0.35, label='Trips')

    ax.set_title(chart_title, size=TITLE_FONT_SIZE)

    ax.set_xlabel('Day Of Week', size=LABEL_FONT_SIZE)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels, size=TICK_FONT_SIZE)
    for x in x_markers:
        ax.axvline(x=x, linestyle=':', alpha=0.25, color='k')

    ax.set_ylabel('Trip Count', size=LABEL_FONT_SIZE)

    y_max = weekly_trips.trip_id.max()
    y_max = ceil(y_max/y_scale)*y_scale

    y_ticks = [x for x in range(0, y_max+y_scale, y_scale)]
    for y in y_ticks:
        ax.axhline(y, linestyle=':', color='k', alpha=0.05)

    ax.grid(False)

    if DO_WRITE_CHARTS:
        plt.savefig(file_name)

    plt.show()
    plt.close()

def yearly_mean(df=None):

    years = sorted(df.start_date.dt.year.unique())
    interval = sorted(df.start_date.dt.week.unique())

    yearly_df = pd.DataFrame(index=interval, columns=['dummy'])
    yearly_df.index.names = ['start_date']

    for year in years:
        year_df = df[df.start_date.dt.year == year].copy()
        year_df = year_df.groupby([year_df.start_date.dt.week]).count()['trip_id'].to_frame()
        year_df.columns = [str(year)]

        # merge year to main dataframe
        yearly_df = yearly_df.merge(year_df, left_index=True, right_index=True, how='left')

    yearly_df.drop(['dummy'], axis=1, inplace=True)

    yearly_df['mean_skipped'] = yearly_df.mean(axis=1, skipna=True)

    yearly_df.fillna(0, inplace=True)
    yearly_df['mean'] = yearly_df.mean(axis=1)

    return yearly_df

def plot_yearly_trips(df,
                      chart_title='San Francisco Subscriber Yearly Trip Counts',
                      file_name='../../charts/subscriber_trips_yearly.png',
                      user_group='subs',
                      DO_WRITE_CHARTS=False,
                      significant_dates=significant_dates):


    if user_group == 'subs':
        main_color = sub_color
        alt_color = cust_color
        label_rotation = -30
        text_align  = 0.20
    else:
        main_color = cust_color
        alt_color = sub_color
        label_rotation = 30
        text_align  = 0.9

    yearly_trips = yearly_mean(df)

    x_tick_labels = month_labels

    x_ticks = [x*(53/12)+(53/24) for x in range(0, len(x_tick_labels))]
    x_markers = [x*(53/12) for x in range(1, len(x_tick_labels))]

    plt.subplots(figsize=FIG_SIZE)
    ax = sns.barplot(x = yearly_trips.index , y = 'mean_skipped', data=yearly_trips, color=main_color, alpha = fade_alpha, label='Trips Starting')
    sns.barplot(ax=ax, x = yearly_trips.index , y = '2013', data=yearly_trips, color=main_color, alpha = fade_alpha, label='2013')
    sns.barplot(ax=ax, x = yearly_trips.index , y = '2014', data=yearly_trips, color=main_color, alpha = fade_alpha, label='2014')
    sns.barplot(ax=ax, x = yearly_trips.index , y = '2015', data=yearly_trips, color=main_color, alpha = fade_alpha, label='2015')
    sns.barplot(ax=ax, x = yearly_trips.index , y = '2016', data=yearly_trips, color=main_color, alpha = fade_alpha, label='2016')

    ax.set_title(chart_title, size=TITLE_FONT_SIZE)

    ax.set_xlabel('Date', size=LABEL_FONT_SIZE)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels, size=TICK_FONT_SIZE)
    for x in x_markers:
        ax.axvline(x, linestyle=':', alpha=0.25, color='k')

    for k, v in significant_dates.items():
        # draw line on date
        ax.axvline(x=(v-365/53/2)/365*53, linestyle='-', alpha=1.0, color=alt_color, linewidth=3)

        ax.text((v-365/53/2)/365, text_align, k,
            horizontalalignment='right',
            verticalalignment='baseline',
            rotation=label_rotation,
            transform=ax.transAxes,
            size=TICK_FONT_SIZE, color='w', weight='bold', alpha=1.0, backgroundcolor=(0.0, 0.0, 0.0, 0.5))

    ax.set_ylabel('Trip Count', size=LABEL_FONT_SIZE)

    if DO_WRITE_CHARTS:
        plt.savefig(file_name)
    plt.show()
    plt.close()














# EOF
