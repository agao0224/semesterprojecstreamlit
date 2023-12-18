import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Popular Names')

df = pd.read_csv('nbadata.csv')

df['YEAR'] = None  # Creating the 'Year' column initially with None values
df.loc[:227, 'YEAR'] = 2020
df.loc[228:413, 'YEAR'] = 2010
df.loc[414:595, 'YEAR'] = 2000

#selected_name = st.text_input('Enter a name', 'John') #First field is prompt, second field is default

#name_df = df[df['name'] == selected_name]

#if name_df.empty:
#    st.write('Name not found :(')
#else:
#    fig = px.line(name_df, x = 'year', y = 'n', color = 'sex',
#                  color_discrete_sequence = ['blue','red'])
#    st.plotly_chart(fig)

selected_year = st.selectbox('Select a year', df['YEAR'].unique())

year_df = df[df['YEAR'] == selected_year]
#fnames = year_df[year_df['sex'] == 'F'].sort_values(by = 'n', ascending = False).head(5)
#mnames = year_df[year_df['sex'] == 'M'].sort_values(by = 'n', ascending = False).head(5)
top_players_2020 = df[df['YEAR'] == 2020].nsmallest(10, 'RANK')
top_players_2010 = df[df['YEAR'] == 2010].nsmallest(10, 'RANK')
top_players_2000 = df[df['YEAR'] == 2000].nsmallest(10, 'RANK')

merged_df = [top_players_2020, top_players_2010, top_players_2000]

top_10_players = pd.concat(merged_df)

#top_names = pd.concat([fnames, mnames], axis = 0) 

st.write(f'Top 10 in {selected_year}:')
st.dataframe(top_10_players)
