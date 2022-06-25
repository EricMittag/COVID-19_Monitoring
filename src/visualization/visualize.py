import logging
import pandas as pd
import plotly.express as px

##Goals
#Generate graphs for deliveries

#Globals

def loadData():
  return pd.read_csv('data/processed/owid_processed_data.csv', sep=";")

def generateTotalCasesLinePlot_norm(df):
  fig = px.line(df, x="date", y="total_cases_norm", color="location", title="Relative Covid Cases Over Time",
                labels={
                     "date": "Date",
                     "total_cases_norm": "Relative Covid Cases to Population",
                     "location": "Country"
                })
  fig_name = 'relativeCases.jpg'
  img_size = 2
  fig.write_image("reports/figures/"+fig_name, width=img_size*700, height=img_size*500)

def generateVaccinatedPeopleLinePlot_norm(df):
  fig = px.line(df, x="date", y="people_vaccinated_norm", color="location", title="Vaccination Rate (at least vaccination)",
                labels={
                     "date": "Date",
                     "people_vaccinated_norm": "Vaccination Rate",
                     "location": "Country"
                })
  fig_name = 'vaccinationRate.jpg'
  img_size = 2
  fig.write_image("reports/figures/"+fig_name, width=img_size*700, height=img_size*500)

def main():
  """ Runs scripts to generate plots
  """
  logger = logging.getLogger(__name__)
  logger.info('Generating Plots')

  df = loadData()
  generateTotalCasesLinePlot_norm(df)
  generateVaccinatedPeopleLinePlot_norm(df)

  logger.info('Plots completed!')


if __name__ == '__main__':
  log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  
  main()
  