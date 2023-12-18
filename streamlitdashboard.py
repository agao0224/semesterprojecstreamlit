import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Popular Names')

df = pd.read_csv('nbadata.csv')

#Filter data with old team names to their new respective team names
df['TEAM'].replace(to_replace = ['NOH'], value = 'NOP', inplace = True)
df['TEAM'].replace(to_replace = ['SEA'], value = 'OKC', inplace = True)
df['TEAM'].replace(to_replace = ['VAN'], value = 'MEM', inplace = True)
df['TEAM'].replace(to_replace = ['CHA'], value = 'CHH', inplace = True)
df['TEAM'].replace(to_replace = ['NJN'], value = 'BKN', inplace = True)

#Organize the dataset by years players played in
df['YEAR'] = None  
df.loc[:227, 'YEAR'] = 2020
df.loc[228:413, 'YEAR'] = 2010
df.loc[414:595, 'YEAR'] = 2000

selected_year = st.selectbox('Select a year', df['YEAR'].unique())

year_df = df[df['YEAR'] == selected_year]

#Get the top 10 players in each decade
top_players_2020 = df[df['YEAR'] == 2020].nsmallest(10, 'RANK')
top_players_2010 = df[df['YEAR'] == 2010].nsmallest(10, 'RANK')
top_players_2000 = df[df['YEAR'] == 2000].nsmallest(10, 'RANK')

merged_df = [top_players_2020, top_players_2010, top_players_2000, top_players_2000]

top_10_players = pd.concat([top_players_2020, top_players_2010], axis = 0)

st.write(f'Top 10 in players in {selected_year}:')
st.dataframe(top_10_players)
