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

def univariate_stats(df, gen_charts):
     output_df = pd.DataFrame(columns=['Count', 'Null', 'Unique', 'Type', 'Min', 'Max', '25%', '50%', '75%', 'Mean', 'Mode', 'Std', 'Skew', 'Kurt'])

     for col in df:
         if pd.api.types.is_numeric_dtype(df[col]):
             oRow = [df[col].count(), df[col].isna().sum(), df[col].nunique(), df[col].dtype, df[col].min(), df[col].max(),
                     df[col].quantile(0.25), df[col].median(), df[col].quantile(0.75), round(df[col].mean(), 2),
                     round(df[col].mode()[0], 2), df[col].std(), df[col].skew(), df[col].kurt()]
             output_df.loc[col] = oRow

             if gen_charts:
                 fig = px.histogram(df, x=col, title=f'Histogram for {col}')
                 st.plotly_chart(fig)

         else:
             oRow = [df[col].count(), df[col].isna().sum(), df[col].nunique(), df[col].dtype, '-', '-', '-', '-', '-',
                     '-', df[col].mode()[0], '-', '-']
             output_df.loc[col] = oRow

             if gen_charts:
                 fig = px.bar(df[col].value_counts().iloc[:6], title=f'Count Plot for {col}')
                 st.plotly_chart(fig)

     return output_df

df_filtered = df.drop(columns=['PLAYER_ID', 'PLAYER', 'TEAM', 'TEAM_ID'])

st.title('NBA Stats Distributions')
selected_stat = st.selectbox('Select a statistic', df_filtered.columns)
generate_chart = st.checkbox('Generate Chart')

# Display the distribution for the selected statistic
if selected_stat:
    output = univariate_stats(df_filtered, selected_stat, generate_chart)
    st.write('Summary Stats:', output)
