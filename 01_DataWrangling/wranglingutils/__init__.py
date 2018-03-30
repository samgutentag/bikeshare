

import datetime
import pandas as pd
from glob import glob



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
            time_marker('\tFinished file! ({:>2d} of {:>2d})'.format(ii+1, len(file_list)))
        elif file_count >= 50 and file_count < 1000:
            if ii % 100 == 0 or ii == 0 or ii == file_count:
                time_marker('\tFinished file! ({:>4d} of {:>4d})'.format(ii+1, len(file_list)))
        else:
            if ii % 1000 == 0 or ii == 0 or ii == file_count:
                time_marker('\tFinished file! ({:>5d} of {:>5d})'.format(ii+1, len(file_list)))

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


def landmark_to_zip(row):
    ''' Return zipcode for given landmark'''
    if row['landmark'] == 'San Francisco':
       return 94107
    if row['landmark'] == 'Redwood City':
        return 94063
    if row['landmark'] == 'Palo Alto':
        return 94301
    if row['landmark'] == 'Mountain View':
        return 94041
    if row['landmark'] == 'San Jose':
        return 95113
    return 99999

def zip_to_landmark(zip_code):
    ''' Return zipcode for given landmark'''
    if zip_code == 94107:
        return 'San Francisco'
    if zip_code == 94063:
        return 'Redwood City'
    if zip_code == 94301:
        return 'Palo Alto'
    if zip_code == 94041:
        return 'Mountain View'
    if zip_code == 95113:
        return 'San Jose'
    return False


# EOF
