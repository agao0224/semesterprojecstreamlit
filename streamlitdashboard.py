import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Top Players in each Decade')

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

#Get the top 10 players in each decade
top_players_2020 = df[df['YEAR'] == 2020].nsmallest(10, 'RANK')
top_players_2010 = df[df['YEAR'] == 2010].nsmallest(10, 'RANK')
top_players_2000 = df[df['YEAR'] == 2000].nsmallest(10, 'RANK')

top_10_players = pd.concat([top_players_2020, top_players_2010, top_players_2000], axis=0)

# Create a dropdown for selecting the decade
selected_decade = st.selectbox('Select a decade', [2020, 2010, 2000])

# Filter data based on the selected decade
selected_decade_df = top_10_players[top_10_players['YEAR'] == selected_decade]

# Display top 10 ranked players for the selected decade
st.write(f'Top 10 players in {selected_decade}:')
st.dataframe(selected_decade_df)
