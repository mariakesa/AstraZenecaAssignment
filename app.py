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
  dat_cntr=dat['country_code'].dropna()
  countries=pd.read_csv(countries_path)
  countries.rename(columns={'country':'country_code'},inplace=True)
  countries_geo=pd.merge(dat_cntr,countries,on='country_code')
  return dat,countries_geo


path='25100_dat.csv'
#Countries downloaded from 'https://developers.google.com/public-data/docs/canonical/countries_csv')
countries_path='countries.csv'
full_data,countries_data=load_data(path,countries_path)
st.subheader('Raw data')
if st.checkbox("Show Raw Data", False):
    st.write(full_data)

st.map(countries_data)
