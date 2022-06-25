import pandas as pd
import requests
import json
import os

def get_from_owid():
  print("Our WORLD IN DATA")

  url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
  #change separator and save to structure
  df = pd.read_csv(url, sep=',')
  df.to_csv('data/raw/owid_full_data.csv', ';')


def get_from_rki():
  print("ROBERT KOCH INSTITUT DATA")
  
  data=requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronafälle_in_den_Bundesländern/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')
  json_object=json.loads(data.content)
  full_list=[]
  for pos,each_dict in enumerate (json_object['features'][:]):
    full_list.append(each_dict['attributes'])

  pd_full_list=pd.DataFrame(full_list)
  pd_full_list.to_csv('data/raw/rki_GER_state_data.csv',sep=';')
  #print(' Number of regions rows: '+str(pd_full_list.shape[0]))

  pd_full_list.info()
  pd_full_list

if __name__ == '__main__':
  #Get Current Dir
  print(os.getcwd())
  get_from_owid()


