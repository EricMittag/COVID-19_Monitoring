import git
import pandas as pd
import numpy as np
import requests
import json
import os 

print(os.getcwd())

import subprocess
import os


def get_from_owid():
  print("Our WORLD IN DATA")

  

def get_from_john_hopkins():
  print("JOHN HOPKINS DATA")

  r = git.Git('data/raw/john_hopkins')
  print(r.pull('https://github.com/CSSEGISandData/COVID-19.git', allow_unrelated_histories=True))

  #1. Clone neu
  #2. Pull

def get_from_rki():
  print("ROBERT KOCH INSTITUT DATA")
  
  data=requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronafälle_in_den_Bundesländern/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')
  json_object=json.loads(data.content)
  full_list=[]
  for pos,each_dict in enumerate (json_object['features'][:]):
    full_list.append(each_dict['attributes'])

  pd_full_list=pd.DataFrame(full_list)
  pd_full_list.to_csv('data/raw/rki_GER_state_data.csv',sep=';')
  print(' Number of regions rows: '+str(pd_full_list.shape[0]))

  pd_full_list.info()
  pd_full_list

if __name__ == '__main__':
  get_from_owid()
  #get_from_john_hopkins()
  get_from_rki()


