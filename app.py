import streamlit as st
import pandas as pd
import plotly.express as px

'''
Do 'pip install streamlit'
To run type: "streamlit run app.py" in the terminal.
'''
#Countries:https://developers.google.com/public-data/docs/canonical/countries_csv
from streamlit import caching

caching.clear_cache()

def prepare_death_disabling_geo(df):
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
    death_geo_grouped=death_geo.groupby(['country_code','year']).sum().reset_index()
    #death_geo_grouped['country_code']=death_geo_grouped.index
    return death_geo, death_geo_grouped

@st.cache(persist=True)
def load_data(path,flat_path,countries_path,alpha_path):
  dat=pd.read_csv(path)
  dat['year']=dat['date'].map(lambda x: int(str(x)[:4]))
  dat_flat=pd.read_csv(flat_path)
  dat_flat['year']=dat_flat['date'].map(lambda x: int(str(x)[:4]))
  dat.rename(columns={'country':'country_code'},inplace=True)
  dat_cntr=dat['country_code'].dropna()
  countries=pd.read_csv(countries_path)
  countries.rename(columns={'country':'country_code'},inplace=True)
  countries_geo=pd.merge(dat_cntr,countries,on='country_code')
  #Death map
  death_geo,death_geo_grouped=prepare_death_disabling_geo(dat)
  #death_geo.rename(columns={'country_code':'deaths'},inplace=True)
  return dat,dat_flat,countries_geo, death_geo,death_geo_grouped


path='25100_dat.csv'
flat_path='25100_flat.csv'
#Countries downloaded from 'https://developers.google.com/public-data/docs/canonical/countries_csv')
countries_path='countries.csv'
alpha_path='alpha_2_3.csv'
full_data,dat_flat,countries_data,death_geo,death_geo_grouped=load_data(path,flat_path,countries_path,alpha_path)
st.subheader('Raw data')
if st.checkbox("Show Raw Data", False):
    st.write(full_data)



st.header('Deaths and disabling events on a map, in the year 2014 (country data only available for that year)')
st.markdown('#### You can toggle between deaths and disabling events and hover over the map to see the number of cases per country.')

select_d=st.selectbox('Event type',['Deaths','Disabling events'],key=1)

if select_d=='Deaths':
    #st.write(death_geo_grouped)
    fig = px.choropleth(death_geo_grouped, locations='country_code',
                        color="death", # lifeExp is a column of gapminder
                        hover_name="death", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
elif select_d=='Disabling events':
    fig = px.choropleth(death_geo_grouped, locations='country_code',
                        color="disabling", # lifeExp is a column of gapminder
                        hover_name="disabling", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

@st.cache()
def plot_yearly_meds_indiv():
    meds_per_year=dat_flat.loc[dat_flat['year']==sl].groupby(['flat_meds'])['medications'].size().sort_values(ascending=False).head(10).to_frame()
    return meds_per_year

st.header('Top 10 sorted occurrence of individual medications yearly')
st.markdown('#### Here we plot the sorted occurence of individual medications as a histogram for every year in the dataset.')
sl=st.slider('Year',2004,2014)
meds_per_year=plot_yearly_meds_indiv()
st.write(meds_per_year)
st.bar_chart(meds_per_year)
plot_yearly_meds_indiv()

#px.histogram('Death and disability histogram')
