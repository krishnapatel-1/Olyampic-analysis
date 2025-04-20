import pandas as pd


def preprocess(df,region_df):


  #filtering for summer olympic
  df=df[df['Season']=='Summer']

  #mergin with region
  df=df.merge(region_df,on='NOC',how='left')

  #dropping dulicate
  df.drop_duplicates(inplace=True)

  #one hote encoding
  df=pd.concat([df,pd.get_dummies (df['Medal'])],axis=1)
  return df
