import urllib.request
from datetime import datetime
import json
import os
from math import ceil, floor
import sched, time
import numpy as np


import pandas as pd


def get_stream_json(feed_url="https://gbfs.fordgobike.com/gbfs/en/station_status.json",
                        time_zone='America/Los_Angeles',
                        time_adjustment=pd.Timedelta('00:00:00'),
                        time_adjust_forward=False):

    # make json request across network
    df = pd.DataFrame()
    try:
        with urllib.request.urlopen(feed_url) as url:
            url_json_response = json.loads(url.read().decode())
    except:
        print('\tURL %s had no response, skipping...' % feed_url)
        return False

    df = pd.DataFrame(url_json_response['data'])
    df = pd.concat([df.drop(['stations'], axis=1), df['stations'].apply(pd.Series)], axis=1)

    # without these columns, we cant perform analysis
    if 'num_bikes_available' not in df.columns or 'num_docks_available' not in df.columns or 'last_reported' not in df.columns:
        print('\tFeed %s does not have required data, skipping...' % feed_url)
        return False

    # drop null values in
    df[df.last_reported == np.nan] = 0

    df['last_reported']          = df['last_reported'].astype('int', errors = 'ignore')
    df['num_bikes_available']    = df['num_bikes_available'].astype('int', errors = 'ignore')
    df['num_docks_available']    = df['num_docks_available'].astype('int', errors = 'ignore')

    try:
        df['last_reported'] = pd.to_datetime(df['last_reported'],unit='s')
    except:
        df['last_reported'] = pd.to_datetime(df['last_reported'],unit='ms')


    # correct time_zone
    if time_adjust_forward:
        df['last_reported'] = df['last_reported'] + time_adjustment
    else:
        df['last_reported'] = df['last_reported'] - time_adjustment

    df.set_index('last_reported', inplace=True)
    try:
        df.tz_localize(time_zone)
    except:
        pass

    df.reset_index(inplace=True)

    return df

def df_to_csv(df, file_dir, file_path):

    if len(df) == 0:
        print('\tDataframe contained no data, skipping...')
        return False

    # make sure directory exists
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if os.path.exists(file_path):
        # append if already exists
        with open(file_path, 'a') as f:
            df.to_csv(f, index=False, header=False)
    else:
        # make a new file if not
        with open(file_path, 'w') as f:
            df.to_csv(f, index=False, header=True)

    return True


def stream_gbfs_feed_json_to_csv(feed_url="https://gbfs.fordgobike.com/gbfs/en/station_status.json",
                                    program_id='babs',
                                    feed_name='system_status',
                                    time_zone='America/Los_Angeles',
                                    time_adjustment=pd.Timedelta('00:00:00'),
                                    time_adjust_forward = False,
                                    file_interval = 30):

    df = get_stream_json(feed_url=feed_url, time_zone=time_zone, time_adjustment=time_adjustment, time_adjust_forward=time_adjust_forward)

    # Timestamp file
    dt = datetime.now()
    m = floor(dt.minute/file_interval)*file_interval
    tstamp = '{:04d}{:02d}{:02d}{:02d}{:02d}'.format(dt.year, dt.month, dt.day, dt.hour, m)

    program_id = program_id.replace('_', '')

    file_dir = 'streamed_data/%s/' % (program_id.lower())
    file_name = 'streamed_data/%s/%s_%s_data_%s.csv' % (program_id.lower(),
                                                            program_id.lower(),
                                                            feed_name.lower(),
                                                            tstamp)

    df_to_csv(df, file_dir, file_name)

    return True



def get_stream(feed_url, program_id, time_zone, time_adjustment, time_adjust_forward = False):
    print('[%s] - Fetching feed from \'%s\'...' % (datetime.now().time(), feed_url))
    try:
        stream_gbfs_feed_json_to_csv(feed_url = feed_url,
                                        program_id=program_id,
                                        feed_name=feed_url.split('/')[-1][:-5],
                                        time_zone = time_zone,
                                        time_adjustment = time_adjustment,
                                        time_adjust_forward=time_adjust_forward)
    except:
        # print('---- Something went wrong, moving on ----')
        pass


def main():

    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc,):

        # International
        get_stream(time_zone = 'America/Toronto', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'sobi_hamilton',               feed_url = 'https://hamilton.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Toronto', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'velgo',                       feed_url = 'http://velogo.ca/opendata/station_status.json') # FEED IS EMPTY
        get_stream(time_zone = 'Asia/Dubai', time_adjustment = pd.Timedelta('4:00:00'), time_adjust_forward = True, program_id = 'ABU',                         feed_url = 'https://api-core.bikeshare.ae/gbfs/gbfs/en/station_status.json')
        get_stream(time_zone = 'Europe/Prague', time_adjustment = pd.Timedelta('1:00:00'), time_adjust_forward = True, program_id = 'velonet_cz',                  feed_url = 'http://velonet.cz/opendata/station_status.json')
        get_stream(time_zone = 'Australia/Melbourne', time_adjustment = pd.Timedelta('10:00:00'), time_adjust_forward = True, program_id = 'monash_bike_share',           feed_url = 'https://monashbikeshare.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Montreal', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bike_share_toronto',          feed_url = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status')
        # get_stream(time_zone = 'Australia/Perth', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = True, program_id = 'curtin_university',           feed_url = 'http://curtinbikeshare.com/opendata/station_status.json')


        # Mountain Time
        get_stream(time_zone = 'America/Denver', time_adjustment = pd.Timedelta('7:00:00'), time_adjust_forward = False, program_id = 'boise_greenbike',             feed_url = 'http://boise.greenbike.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Denver', time_adjustment = pd.Timedelta('7:00:00'), time_adjust_forward = False, program_id = 'bcycle_boulder',              feed_url = 'https://gbfs.bcycle.com/bcycle_boulder/station_status.json')
        get_stream(time_zone = 'America/Denver', time_adjustment = pd.Timedelta('7:00:00'), time_adjust_forward = False, program_id = 'bcycle_denver',               feed_url = 'https://gbfs.bcycle.com/bcycle_denver/station_status.json')
        get_stream(time_zone = 'America/Denver', time_adjustment = pd.Timedelta('7:00:00'), time_adjust_forward = False, program_id = 'bcycle_greenbikeslc',         feed_url = 'https://gbfs.bcycle.com/bcycle_greenbikeslc/station_status.json')
        get_stream(time_zone = 'America/Denver', time_adjustment = pd.Timedelta('7:00:00'), time_adjust_forward = False, program_id = 'mountain_rides_bike_share',   feed_url = 'http://mrbikeshare.org/opendata/station_status.json')

        # Central Time
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_nashville',            feed_url = 'https://gbfs.bcycle.com/bcycle_nashville/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_austin',               feed_url = 'https://gbfs.bcycle.com/bcycle_austin/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bike_chattanooga',            feed_url = 'https://gbfs.bikechattanooga.com/gbfs/gbfs/en/station_status.json') # replaced by new feed
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_bublr',                feed_url = 'https://gbfs.bcycle.com/bcycle_bublr/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_clarksville',          feed_url = 'https://gbfs.bcycle.com/bcycle_clarksville/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_dallasfairpark',       feed_url = 'https://gbfs.bcycle.com/bcycle_dallasfairpark/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_desmoines',            feed_url = 'https://gbfs.bcycle.com/bcycle_desmoines/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_elpaso',               feed_url = 'https://gbfs.bcycle.com/bcycle_elpaso/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_fortworth',            feed_url = 'https://gbfs.bcycle.com/bcycle_fortworth/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_greatrides',           feed_url = 'https://gbfs.bcycle.com/bcycle_greatrides/station_status.json')     # feed is empty...
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_heartland',            feed_url = 'https://gbfs.bcycle.com/bcycle_heartland/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_houston',              feed_url = 'https://gbfs.bcycle.com/bcycle_houston/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_kc',                   feed_url = 'https://gbfs.bcycle.com/bcycle_kc/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_madison',              feed_url = 'https://gbfs.bcycle.com/bcycle_madison/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_mcallen',              feed_url = 'https://gbfs.bcycle.com/bcycle_mcallen/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'niceridemn',                  feed_url = 'https://api-core.niceridemn.org/gbfs/en/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_spokies',              feed_url = 'https://gbfs.bcycle.com/bcycle_spokies/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_rapidcity',            feed_url = 'https://gbfs.bcycle.com/bcycle_rapidcity/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'bcycle_sanantonio',           feed_url = 'https://gbfs.bcycle.com/bcycle_sanantonio/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'topeka_metro_bikes',          feed_url = 'http://topekametrobikes.org/opendata/station_status.json')
        get_stream(time_zone = 'America/Chicago', time_adjustment = pd.Timedelta('6:00:00'), time_adjust_forward = False, program_id = 'divvy',                       feed_url = 'https://gbfs.divvybikes.com/gbfs/en/station_status.json')

        # Pacific Time
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'biketown_pdx',            feed_url = 'http://biketownpdx.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'bishop_ranch',            feed_url = 'http://britebikes.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'breeze_bikeshare',        feed_url = 'http://santamonicabikeshare.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'grid_bike_share',         feed_url = 'https://grid.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'bcycle_rtcbikeshare',     feed_url = 'https://gbfs.bcycle.com/bcycle_rtcbikeshare/station_status.json')
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'bcycle_lametro',          feed_url = 'https://gbfs.bcycle.com/bcycle_lametro/station_status.json')
        get_stream(time_zone = 'America/Los_Angeles', time_adjustment = pd.Timedelta('8:00:00'), time_adjust_forward = False, program_id = 'BA',                      feed_url = 'https://gbfs.fordgobike.com/gbfs/en/station_status.json')

        # Eastern Time
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_columbike',           feed_url = 'https://gbfs.bcycle.com/bcycle_columbike/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_pacersbikeshare',     feed_url = 'https://gbfs.bcycle.com/bcycle_pacersbikeshare/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_arborbike',           feed_url = 'https://gbfs.bcycle.com/bcycle_arborbike/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_aventura',            feed_url = 'https://gbfs.bcycle.com/bcycle_aventura/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_battlecreek',         feed_url = 'https://gbfs.bcycle.com/bcycle_battlecreek/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_broward',             feed_url = 'https://gbfs.bcycle.com/bcycle_broward/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_charlotte',           feed_url = 'https://gbfs.bcycle.com/bcycle_charlotte/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_cincyredbike',        feed_url = 'https://gbfs.bcycle.com/bcycle_cincyredbike/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_clemson',             feed_url = 'https://gbfs.bcycle.com/bcycle_clemson/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'coast_bike_share',           feed_url = 'http://coast.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_columbiacounty',      feed_url = 'https://gbfs.bcycle.com/bcycle_columbiacounty/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_greenville',          feed_url = 'https://gbfs.bcycle.com/bcycle_greenville/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_indego',              feed_url = 'https://gbfs.bcycle.com/bcycle_indego/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_jacksoncounty',       feed_url = 'https://gbfs.bcycle.com/bcycle_jacksoncounty/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'juice_bike_share',           feed_url = 'https://www.juicebikeshare.com/opendata/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_linkdayton',          feed_url = 'https://gbfs.bcycle.com/bcycle_linkdayton/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'reddy_bikeshare',            feed_url = 'https://reddybikeshare.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'relay_bike_share',           feed_url = 'https://relaybikeshare.socialbicycles.com/opendata/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_catbike',             feed_url = 'https://gbfs.bcycle.com/bcycle_catbike/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'sobi_long_beach',            feed_url = 'http://sobilongbeach.com/opendata/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'bcycle_spartanburg',         feed_url = 'https://gbfs.bcycle.com/bcycle_spartanburg/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'university_of_virginia',     feed_url = 'http://ubike.virginia.edu/opendata/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'cabi',                       feed_url = 'https://gbfs.capitalbikeshare.com/gbfs/en/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'NYC',                        feed_url = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'cogo',                       feed_url = 'https://gbfs.cogobikeshare.com/gbfs/en/station_status.json')
        get_stream(time_zone = 'America/New_York', time_adjustment = pd.Timedelta('5:00:00'), time_adjust_forward = False, program_id = 'hubway',                     feed_url = 'https://gbfs.thehubway.com/gbfs/en/station_status.json')


        # New Programs!
        get_stream(time_zone = 'America/Curacao',       time_adjustment = pd.Timedelta('4:00:00'),      time_adjust_forward = False, program_id = 'aru',                feed_url = 'https://aru.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'America/Fortaleza',     time_adjustment = pd.Timedelta('3:00:00'),      time_adjust_forward = False, program_id = 'rec',                feed_url = 'https://rec.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'Atlantic/Reykjavik',    time_adjustment = pd.Timedelta('0:00:00'),      time_adjust_forward = False, program_id = 'rey',                feed_url = 'https://rey.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'America/Mexico_City',   time_adjustment = pd.Timedelta('6:00:00'),      time_adjust_forward = False, program_id = 'guad',               feed_url = 'https://guad.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'America/Denver',        time_adjustment = pd.Timedelta('7:00:00'),      time_adjust_forward = False, program_id = 'asp',                feed_url = 'https://asp.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'America/Chicago',       time_adjustment = pd.Timedelta('6:00:00'),      time_adjust_forward = False, program_id = 'chat',               feed_url = 'https://chat.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'America/Chicago',       time_adjustment = pd.Timedelta('6:00:00'),      time_adjust_forward = False, program_id = 'lou',                feed_url = 'https://lou.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'America/New_York',      time_adjustment = pd.Timedelta('5:00:00'),      time_adjust_forward = False, program_id = 'det',                feed_url = 'https://det.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'Pacific/Honolulu',      time_adjustment = pd.Timedelta('10:00:00'),     time_adjust_forward = False, program_id = 'kona',               feed_url = 'https://kona.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')
        get_stream(time_zone = 'Pacific/Honolulu',      time_adjustment = pd.Timedelta('10:00:00'),     time_adjust_forward = False, program_id = 'hon',                feed_url = 'https://hon.publicbikesystem.net/ube/gbfs/v1/en/station_status.json')



        seconds = 60
        print('\t[%s] - Waiting %s minutes to run again...\n' % (datetime.now().time(), INTERVAL))
        s.enter(INTERVAL*seconds, 1, do_something, (sc,))


    s.enter(0, 1, do_something, (s,))
    s.run()

    return True




if __name__ == '__main__':

    global INTERVAL
    INTERVAL = 5

    main()
