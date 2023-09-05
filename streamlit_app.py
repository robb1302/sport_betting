import streamlit as st
import pandas as pd
from src.data.download import download_fixtures 
import os
import streamlit_analytics

streamlit_analytics.start_tracking()



# Center-align the title using HTML and CSS style
st.write(
    """
    <div style="text-align: center;">
        <h2> Welcome to </h2>
        <h1>🍀The Gamblin' Goblin🍀</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# if st.button('Getting Started'):
#     st.balloons()

# Path to your local CSV file
# download_fixtures()

# Read the CSV file into a DataFrame
df = pd.read_csv("data/results/results.csv", index_col=0)

# Display the DataFrame as a table
# st.write("Upcoming Games")

# Sidebar filter options
st.sidebar.header('Filter League')

# Create a selectbox widget for selecting a specific Div value
selected_div = st.sidebar.selectbox('Select Division', df['Div'].unique())

# Filter the DataFrame based on the selected Div value
filtered_df = df[df['Div'] == selected_div]

# Display the filtered DataFrame
st.dataframe(filtered_df, hide_index=True)

streamlit_analytics.stop_tracking()
