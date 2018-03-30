# Bay Area Bike Share Ridership
This project uses data reported by the Bay Area Bike Share (currently Ford Go Bike) program in San Francisco, California and surrounding Bay Area cities.

The Bay Area Bike Share Program was revamped and rebranded to Ford Go Bike in 2017 and has expanded its reach

# Results
The best Sub Topic Groupings were generated using an Online Latent Dirichlet Allocation model provided by `genesis`.  This Model was trained to identify 50 Topics, with 10 Terms per topic, and given 50 Passes to process the review texts.

Text was tokenized and lemmatized, so that we retained complete English readable words (vs stemming).  The corpus was restricted to only tokens appearing more frequently than the 10,000th most frequently token.  Example	 if the 10,000th token appeared just 3 times, only tokens occurring 4 or more times were kept.

This processing took nearly 13 hours to complete on a 2010 MacBook Pro, so please take that into consideration when attempting to recreate these results.

## Identified Sub Topics


## Assigning Topics to Reviews

## Calculating Restaurant Sub Topic Stars

## Identifying the Most Influential Sub Topics

## Comparison Reporting Tool


# Reproduce my Work
Few simple steps to get started and reproduce my work.

## Getting Started
Clone this repo to get started.  From there, if you are using `conda` to manage your virtual environment, run the following command to setup the environment and install the needed packages.  Be sure to pass the included `environment.yml` file.

```
# conda env create environment.yml
```

## Prerequisites
### Directory Structure

Once you have your environment set up, you will need to create some extra directories for your files.

### Env Variables

google maps API
darksky API


```
# python -m nltk.downloader all
# python -m spacy download en
```

Lastly, the data used for this project is supplied by the [Yelp Open Dataset](https://www.yelp.com/dataset).  You will need to download a copy of the source data and store it in a directory called `source_data` to run these notebooks without making changes to any code.

Specifically, you will need to copy over `business.json` and `review.json` from the downloaded data set to the `source_data` directory.

The starter directory structure should look like this:

```
yelpsubtopics
| -README.md
| -environment.yml
| -.gitignore
| -models
| -clean_data
| -source_data
|   |- business.json
|   |- review.json
| -documents
| -DataWrangling
|   |- 00_Business_Data_Wrangling.ipynb
|   |- 01_Review_Wrangling.ipynb
| -TopicModelling
|   |- model_03a_all_reviews_nouns.ipynb
|   |- model_05_all_reviews.ipynb
|   |- model_02_nff_reviews.ipynb
|   |- MODEL_SUMMARY.ipynb
|   |- model_01_ff_reviews.ipynb
|   |- model_04_all_reviews_nouns_verbs.ipynb
| -SubTopicReviews
|   |- SubTopicTagging_Model5.ipynb
|   |- SubTopic_Investigation.ipynb
|   |- plottingtools
|       |- init__.py
| -scripts
|   |- clean_checkins.py
|   |- clean_users.py
| -charts
|   |- reports
```

## Step 00 - Data Wrangling
Each of the provided data sets is moderately well formatted and abides by the [Global Bike Share Feed Specification](https://github.com/NABSA/gbfs) for data presentation.

Downloaded data is in the format of  


### Stations Data
The stations data is in a collection of 4 files, each including the status of all stations that are active at the time the data was collected.  Additionally, Bay Area Bike Share published a `README.txt` file with each data set that includes notes on station expansion and relocation dates.

For each station, drop duplicated rows, reported when a station does not move or change between data collection times.
Next we attend to each note included in the `README` files, example Station

Data Columns
| `station_id`         | (string)   | number ID for the station                                                                                                             |
|----------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `station_name`       | (string)   | name of the station                                                                                                                   |
| `lat`                | (float)    | latitude coordinate of the station                                                                                                    |
| `long`               | (float)    | longitude coordinate of the station                                                                                                   |
| `dock_count`         | (int)      | number of docks at the station                                                                                                        |
| `region`             | (string)   | city/service area the station is located within                                                                                       |
| `first_service_date` | (datetime) | date that the station became active                                                                                                   |
| `last_service_date`  | (datetime) | date that the station became inactive else the final date in the recorded data (gathered from `trips_data` last trip completion date) |
| `zip_code`           | (int)      | zip code the station is located within                                                                                                |
| `days_in_service`    | (int)      | `last_service_date` - `first_service_date`                                                                                            |
| `elevation_meters`   | (float)    | collected from polling the Google Maps Elevation API                                                                                  |
| `elevation_feet`     | (float)    | meters converted to feet by dividing `elevatoin_meters` by 0.3048                                                                     |

### Dark Sky Data


### Trip Data





# Additional Information
## Authors
* **Sam Gutentag** - *Initial work* - [samgutentag](www.samgutentag.com)

See other projects by Sam on [Github](https://github.com/samgutentag)

## Acknowledgments
* The [Yelp Open Data Set](https://www.yelp.com/dataset)
* [Simon Worgan](https://www.linkedin.com/in/simon-worgan-44613138/)
* [Springboard](www.springboard.com)


#datascience #github
#datascience
