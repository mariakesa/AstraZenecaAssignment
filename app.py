import streamlit as st
import pandas as pd
import pydeck as pdk

'''
Do 'pip install streamlit'
To run type: "streamlit run app.py" in the terminal.
'''
#Countries:https://developers.google.com/public-data/docs/canonical/countries_csv
from streamlit import caching

caching.clear_cache()

def prepare_death_geo(df):
    death_df=df.copy()
    alpha=pd.read_csv(alpha_path,header=0)
    #alpha.rename(columns={'Alpha-2 code':'country_code'},inplace=True)
    #print(death_df)
    alpha['country_code'] = alpha['country_code'].map(lambda x: x.replace('\"','').strip())
    alpha['Alpha-3 code'] = alpha['Alpha-3 code'].map(lambda x: x.replace('\"','').strip())
    cntr_dict={}
    for ind in range(0,alpha.shape[0]):
      cntr_dict[alpha.iloc[ind]['country_code']]=alpha.iloc[ind]['Alpha-3 code']
    death_geo = death_df[death_df['country_code'].notna()]
    death_geo['country_code']=death_geo['country_code'].map(cntr_dict)
    death_geo=death_geo.groupby(['country_code']).sum()
    death_geo['country_code']=death_geo.index
    return death_geo


@st.cache(persist=True)
def load_data(path,countries_path,alpha_path):
  dat=pd.read_csv(path)
  dat.rename(columns={'country':'country_code'},inplace=True)
  dat_cntr=dat['country_code'].dropna()
  countries=pd.read_csv(countries_path)
  countries.rename(columns={'country':'country_code'},inplace=True)
  countries_geo=pd.merge(dat_cntr,countries,on='country_code')
  #Death map
  death_geo=prepare_death_geo(dat)
  #death_geo.rename(columns={'country_code':'deaths'},inplace=True)
  return dat,countries_geo, death_geo


path='25100_dat.csv'
#Countries downloaded from 'https://developers.google.com/public-data/docs/canonical/countries_csv')
countries_path='countries.csv'
alpha_path='alpha_2_3.csv'
full_data,countries_data,death_geo=load_data(path,countries_path,alpha_path)
st.subheader('Raw data')
if st.checkbox("Show Raw Data", False):
    st.write(full_data)

st.map(countries_data)

st.write(death_geo)

import plotly.express as px

fig = px.choropleth(death_geo, locations='country_code',
                    color="death", # lifeExp is a column of gapminder
                    hover_name="death", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)
'''
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[
    pdk.Layer(
    "HexagonLayer",
    data=death_geo[['death','latitude','longitude']],
    get_position=['longitude','latitude'],
    radius=100,
    pickable=True,
    elevation_scale=4,
    elevation_range=[0,1000],
    ),
    ],
))
'''
