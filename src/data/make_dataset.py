# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import pandas as pd

##Goals
#Only selected Countries and add needed columns


#Globals
INPUT_PATH = 'data/raw/'
OUTPUT_PATH = 'data/processed/'

list_of_countries = ['Germany', 'United States', 'Israel']
binary_selector = [0] * 3

#@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
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
    df_allSelectedCountries.to_csv(output_filepath + 'owid_processed_data.csv', sep=";")

    logger.info('processing data completed!')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main(INPUT_PATH, OUTPUT_PATH)
