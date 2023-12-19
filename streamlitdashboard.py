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

def univariate_stats(df, col, gen_charts):
    if pd.api.types.is_numeric_dtype(df[col]):
        oRow = [df[col].count(), df[col].isna().sum(), df[col].nunique(), df[col].dtype, df[col].min(), df[col].max(),
                df[col].quantile(0.25), df[col].median(), df[col].quantile(0.75), round(df[col].mean(), 2),
                round(df[col].mode()[0], 2), df[col].std(), df[col].skew(), df[col].kurt()]

        if gen_charts:
            fig = px.histogram(df, x=col, title=f'Histogram for {col}')
            st.plotly_chart(fig)

    else:
        oRow = [df[col].count(), df[col].isna().sum(), df[col].nunique(), df[col].dtype, '-', '-', '-', '-', '-',
                '-', df[col].mode()[0], '-', '-']

        if gen_charts:
            fig = px.bar(df[col].value_counts().iloc[:6], title=f'Count Plot for {col}')
            st.plotly_chart(fig)

    return oRow

df_filtered = df.drop(columns=['PLAYER_ID', 'PLAYER', 'TEAM', 'TEAM_ID'])

st.title('NBA Statistics Distribution')
selected_column = st.selectbox('Select a column', df_filtered.columns)

# Display the distribution for the selected column
if st.button('Generate Chart'):
    output = univariate_stats(df_filtered, selected_column, True)



combined_top_players = pd.concat([top_players_2020, top_players_2010, top_players_2000])

def generate_plot(statistic):
    fig = px.bar(combined_top_players, x='YEAR', y=statistic, color='YEAR',
                 title=f'Average {statistic} of Top 10 Players at the Beginning of Each Decade')
    fig.update_layout(xaxis_title='Year', yaxis_title=f'Average {statistic}')
    st.plotly_chart(fig)

# Streamlit app
st.title('NBA Player Stats Comparison')

# Dropdown for statistics
statistic_options = ['PTS', 'AST', 'REB', 'FG_PCT', 'MIN', 'EFF', 'FG3_PCT', 'FG3M', 'GP']
selected_statistic = st.selectbox('Select a Statistic', statistic_options)

# Generate plot on button click
if st.button('Generate Plot'):
    generate_plot(selected_statistic)
