import streamlit as st
import pandas as pd
from src.data.download import download_fixtures
import os

# Center-align the title using HTML and CSS style
st.write(
    """
    <div style="text-align: center;">
        <h2>Welcome to</h2>
        <h1>The Gamblin' Goblin</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Path to your local CSV file
# download_fixtures()

# Read the CSV file into a DataFrame
df = pd.read_csv("data/results/results.csv")

# Define the default columns to display
default_columns_probs = ["Home Team", "Away Team", "Home Prob", "Draw Prob", "Away Prob"]
default_columns_odds = ["Home Team", "Away Team", "Fair Home Odd", "Fair Draw Odd", "Fair Away Odd"]


# Create a selectbox widget for selecting a specific Div value
selected_div = st.selectbox('Select a League', df['Div'].unique())

# Filter the DataFrame based on the selected Div value
filtered_df = df[df['Div'] == selected_div]

# Initialize the unique identifier
unique_identifier = st.session_state.get('unique_identifier', 0)

# Create a button to toggle the DataFrame
if st.button('Predictions or Odds'):
    # Toggle between the original and modified DataFrame by adding a unique identifier
    unique_identifier += 1
    st.session_state['unique_identifier'] = unique_identifier

# Define the selected columns based on the button's state
selected_columns = default_columns_probs if unique_identifier % 2 == 0 else default_columns_odds

# Center-align the filtered DataFrame within the Streamlit app
st.write(
    "<div style='display: flex; justify-content: center; align-items: center; height: 500px;'>"
    "<div>"
    f"{filtered_df[selected_columns].to_html(index=False, escape=False)}"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)
