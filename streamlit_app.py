import streamlit as st
import pandas as pd
import config as CONFIG
import json

file_path = f"{CONFIG.DATA_FOLDER_MAPPING}league_names.json"
with open(file_path, 'r', encoding='utf-8') as json_file:
    league_names = json.load(json_file)

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

# Read the CSV file into a DataFrame
df = pd.read_csv("data/results/results.csv")
df.Div = df.Div.replace(league_names)

# make betting slip
betting_slip = pd.read_csv("data/results/betting_slip.csv",index_col=False)
betting_slip.Div = betting_slip.Div.replace(league_names)


# Create a selectbox widget for selecting a specific Div value
# Wrap the st.selectbox in a div with custom CSS for width control
with st.container():
    st.markdown('<style>div[data-testid="stSelectbox"] .Select__placeholder {width: 100px;}</style>', unsafe_allow_html=True)
    division = ["All Leagues"] + list(df['Div'].unique())
    selected_div = st.selectbox('Select a League', division)

# Filter the DataFrame based on the selected Div value
if selected_div != "All Leagues":
    filtered_df = df[df['Div'] == selected_div]
    betting_slip_filtered = betting_slip[betting_slip['Div'] == selected_div]
else:
    filtered_df = df
    betting_slip_filtered = betting_slip

# Initialize the unique identifier
unique_identifier = st.session_state.get('unique_identifier', 0)

# Create a button to toggle the DataFrame with the dynamic label
if st.button("Prediction or Betting Slip"):
    # Toggle between the original and modified DataFrame by adding a unique identifier
    unique_identifier += 1
    st.session_state['unique_identifier'] = unique_identifier

# Change with every click
if unique_identifier%2 == 0:
    # Set up HTML and CSS for controlling the table width
    styled_html = f"""
        <div style="width: 800px;">  <!-- Adjust the width as needed -->
            <table>
                {betting_slip_filtered[["Home Team","Away Team","bet on"]].to_html(classes='dataframe', index=False)}
            </table>
        </div>
    """
    st.write("### Matches worth betting on.")
    # Render the HTML content using st.write with unsafe_allow_html=True
    st.write(styled_html, unsafe_allow_html=True)
else:
    # Define the default columns to display
    default_columns_probs = ["Home Team", "Away Team", "Home Prob", "Draw Prob", "Away Prob"]

    styled_html = f"""
        <div style="width: 800px;">  <!-- Adjust the width as needed -->
            <table>
                {filtered_df[default_columns_probs].to_html(classes='dataframe', index=False)}
            </table>
        </div>
    """
    st.write("### The outcome of the matches based on the betting odds.")
    st.write(styled_html, unsafe_allow_html=True)

