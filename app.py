import streamlit as st
import pandas as pd

'''
Do 'pip install streamlit'
To run type: "streamlit run app.py" in the terminal.
'''
#Countries:https://developers.google.com/public-data/docs/canonical/countries_csv
@st.cache(persist=True)
def load_data(path,countries_path):
  dat=pd.read_csv(path)
  dat.rename(columns={'country':'country_code'},inplace=True)
  dat=dat['country_code'].dropna()
  st.write(dat)
  countries=pd.read_csv(countries_path)
  print(countries.columns)
  countries.rename(columns={'country':'country_code'},inplace=True)
  st.write(countries)
  countries_geo=pd.merge(dat,countries,on='country_code')
  st.write(countries_geo)
  return countries_geo


path='25100_dat.csv'
#Countries downloaded from 'https://developers.google.com/public-data/docs/canonical/countries_csv')
countries_path='countries.csv'
data=load_data(path,countries_path)

st.map(data)

st.write(data)
