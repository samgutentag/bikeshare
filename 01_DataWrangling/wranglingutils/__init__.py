

import datetime
import pandas as pd
from glob import glob


import matplotlib
import matplotlib.pyplot as plt
from math import ceil

import datetime

import seaborn as sns
sns.set_style('whitegrid')
sns.set_context("poster")
font = {'size'   : 50}
matplotlib.rc('font', **font)

COLOR_BLU = '#0074C8'
COLOR_YEL = '#FACD6B'
COLOR_GRY = '#71C9BE'
COLOR_GRE = '#85B74A'

LABEL_FONT_SIZE = 15
TITLE_FONT_SIZE = 25
TICK_FONT_SIZE = 10
FIG_SIZE = (15,6)



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


def plot_counts(df,top_n=20,
                color_norm=COLOR_BLU, color_highlight=COLOR_YEL,
                highlight_labels=[],
                x_label='', x_label_rot = 0,
                y_label='', y_interval=25,
                title='', figsize=FIG_SIZE):

    # if highest count is greater than 1000, use logy scale
    if df.max() > 450:
        logy=True
    else:
        logy=False

    # select top n most popular by count
    plot_index = df.sort_values(ascending=False)[:top_n].index
    df = df[df.index.isin(plot_index)]

    color_codes = [color_norm if x not in highlight_labels else color_highlight for x in df.index]
    ax = df.plot(figsize=figsize, kind='bar', logy=logy, color=color_codes)
    ax.set_title('{}'.format(title.title()), size=TITLE_FONT_SIZE, weight='bold')

    ax.set_ylabel('{}'.format(y_label), size=LABEL_FONT_SIZE, weight='bold')
    ax.set_xlabel('{} (top {})'.format(x_label, top_n), size=LABEL_FONT_SIZE, weight='bold')

    # remove spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # y scale and ticks
    if logy:
        mag = len(str(df.max()))
        ax.set_ylabel('{} (log)'.format(y_label), size=LABEL_FONT_SIZE, weight='bold')
        for y in [10**y for y in range(0, mag+1)]:
            ax.axhline(y, linestyle=':', color=COLOR_GRY, zorder=-1)
    else:
        y_max = ceil(df.max()/y_interval)

        ax.set_yticks([y*y_interval for y in range(0, y_max+1)])
        for y in [y*y_interval for y in range(0, y_max+1)]:
            ax.axhline(y, linestyle=':', color=COLOR_GRY, zorder=-1)

    # x tick labels
    ax.set_xticklabels([x for x in df.index], size=TICK_FONT_SIZE, rotation=x_label_rot)

    ax.grid(False)
    plt.tight_layout()
    plt.savefig('../charts/plot_counts_{}_counts.png'.format(title.replace(' ', '_').lower()))
#     print('../charts/{}_counts.png'.format(title.replace(' ', '_').lower()))

    plt.show()
    plt.close()




# EOF
