# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import pandas as pd
import numpy as np

##Goals
#Only selected Countries and add needed columns


#Globals
INPUT_PATH = 'data/raw/'
OUTPUT_PATH = 'data/processed/'

def selectedCountriesCasesVax(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    list_of_countries = ['Germany', 'United States', 'Israel']
    binary_selector = [0] * 3

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    df = pd.read_csv(input_filepath+'owid_full_data.csv', sep=";")

    ##Reduce df to selected countries
    binary_selector[0] = df['location'] == list_of_countries[0]
    binary_selector[1] = df['location'] == list_of_countries[1]
    binary_selector[2] = df['location'] == list_of_countries[2]

    b_allSelectedCountries = (binary_selector[0]|binary_selector[1]|binary_selector[2])

    df_allSelectedCountries = df[b_allSelectedCountries]

    ##Adding normalized columns to dataset
    #Cases
    df_allSelectedCountries['total_cases_norm'] = df_allSelectedCountries['total_cases']/df_allSelectedCountries['population']
    #Vaccinations
    df_allSelectedCountries['people_vaccinated_norm'] = df_allSelectedCountries['people_vaccinated']/df_allSelectedCountries['population']

    ##Saving df to structure
    df_allSelectedCountries.to_csv(output_filepath + 'GER_US_ISR_cases_vax.csv', sep=";")

    logger.info('processing data completed!')

def getRelevantData(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    df = pd.read_csv(input_filepath+'owid_full_data.csv', sep=";", index_col=0)

    #Get Important Cols out of full data set and sort by date
    df_reduced_raw = df[['date', 'location', 'total_cases']].sort_values('date',ascending=True).reset_index(drop=True).copy()

    #rename columns
    df_reduced = df_reduced_raw.rename(columns= {
    'location':'country',
    'total_cases':'confirmed'
    })

    #Cleaning Data: Not enough data
    df_reduced = df_reduced[df_reduced['country']!='Western Sahara']

    #Fill missing values
    df_reduced['confirmed']=df_reduced['confirmed'].fillna(0)

    df_reduced.to_csv(output_filepath + 'Reduced_OWID_Set.csv', sep=";", index=False)
    logger.info('processing data completed!')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    #selectedCountriesCasesVax(INPUT_PATH, OUTPUT_PATH)
    getRelevantData(INPUT_PATH, OUTPUT_PATH)
