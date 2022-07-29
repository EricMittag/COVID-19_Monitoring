"""
Functions for Doubling Rate Calculation and Filtering
"""
import pandas as pd
import numpy as np
from sklearn import linear_model
from scipy import signal

reg = linear_model.LinearRegression(fit_intercept=True)


###Functions
##Helper
#Doubling Rate
def get_doubling_time_via_regression(in_array):
    ''' Use a linear regression to approximate the doubling rate'''

    y = np.array(in_array)
    X = np.arange(-1,2).reshape(-1, 1)

    assert len(in_array)==3
    reg.fit(X,y)
    intercept=reg.intercept_
    slope=reg.coef_

    return intercept/slope

def rolling_reg(df_input,col='confirmed'):
    ''' input has to be a data frame'''
    ''' return is single series (mandatory for group by apply)'''
    days_back=3
    result=df_input[col].rolling(
                window=days_back,
                min_periods=days_back).apply(get_doubling_time_via_regression,raw=False)
    return result

#Filtering
def savgol_filter(df_input,column='confirmed',window=5):
    ''' Savgol Filter which can be used in groupby apply function 
        it ensures that the data structure is kept'''
    degree=1
    df_result=df_input
    filter_in=df_input[column].fillna(0)
    result=signal.savgol_filter(np.array(filter_in),
                           window, # window size used for filtering
                           degree)
    df_result[column+'_filtered']=result
    return df_result

##General
#Doubling Rate
def add_doubling_rate(df_input, col):
  ''' Calculate approximated doubling rate and return merged data frame

    Parameters:
    ----------
    df_input: pd.DataFrame
    col: str
        defines the used column
    Returns:
    ----------
    df_output: pd.DataFrame
        the result will be joined as a new column on the input data frame
  '''
  must_contain=set(['country',col])
  assert must_contain.issubset(set(df_input.columns))

  #Add DR to DF
  df_DR = df_input[['country', col]].groupby('country').apply(rolling_reg,col).reset_index()
  #Renaming Columns 
  df_DR = df_DR.rename(columns={
    col: col + '_DR',
    'level_1':'index'
  })
  #Merge
  df_input = df_input.reset_index()
  df_output = pd.merge(df_input, df_DR[['index',col+'_DR']], on=['index'], how='left')
  df_output = df_output.drop(columns=['index'])

  return df_output

#Filtering
def add_filtered_col(df_input, col):
  '''  Calculate savgol filter and return merged data frame

      Parameters:
      ----------
      df_input: pd.DataFrame
      col: str
          defines the used column
      Returns:
      ----------
      df_output: pd.DataFrame
          the result will be joined as a new column on the input data frame
  '''

  must_contain=set(['country',col])
  assert must_contain.issubset(set(df_input.columns))

  df_output=df_input.copy().reset_index() #prevent overwriting

  df_filtered = df_output[['country',col]].groupby(['country']).apply(savgol_filter).reset_index()
  #Merge
  df_output = pd.merge(df_output, df_filtered[['index', col+'_filtered']],on=['index'],how='left') 

  df_output = df_output.drop(columns=['index'])
  return df_output.copy()



##################################################################################
#MAIN
if __name__ == '__main__':
  df = pd.read_csv('data/processed/Reduced_OWID_Set.csv',sep=';',parse_dates=[0])
  df.sort_values('date',ascending=True).reset_index().copy()
  df_result = add_filtered_col(df, 'confirmed')
  df_result = add_doubling_rate(df_result, 'confirmed')
  df_result = add_doubling_rate(df_result, 'confirmed_filtered')

  #Mask 'bad' data
  mask=df_result['confirmed']>100
  df_result['confirmed_filtered_DR']=df_result['confirmed_filtered_DR'].where(mask, other=np.NaN)
  df_result.to_csv('data/processed/COVID_final_set.csv',sep=';',index=False)

  print(df_result)
  

