import pandas as pd

def transform_and_merge(df,preds):
    """
    Transforms and merges a given DataFrame to create a new DataFrame with columns for home and away teams' predictions
    and a 'preds_draw' column representing the probability of a draw.

    Args:
        df (pd.DataFrame): The input DataFrame containing 'Team', 'Opponent', 'atHome', 'Div', and 'preds' columns.

    Returns:
        pd.DataFrame: A new DataFrame with 'Div', 'Home', 'Away', 'preds_home', 'preds_away', and 'preds_draw' columns.
    """

    # Extract the specified columns and convert 'atHome' to boolean
    preds[["Team", "Opponent", "atHome", "Div"]] = df[["Team", "Opponent", "atHome", "Div"]].values
    preds['atHome'] = preds['atHome'].astype('bool')

    # Create a mask to identify home and away teams
    home_mask = preds['atHome']
    away_mask = ~home_mask

    # Create separate DataFrames for home and away teams
    home_df = preds[home_mask].rename(columns={'Team': 'Home', 'Opponent': 'Away', 'preds': 'preds_home'})
    away_df = preds[away_mask].rename(columns={'Team': 'Away', 'Opponent': 'Home', 'preds': 'preds_away'})

    # Merge the two DataFrames based on the 'Home' and 'Away' columns
    result_df = pd.merge(home_df[["Div", 'Home', 'Away', 'preds_home']], away_df[['Home', 'Away', 'preds_away']], on=['Home', 'Away'])

    # Calculate 'preds_draw' column
    result_df["preds_draw"] = 1 - (result_df["preds_home"] + result_df["preds_away"])

    return result_df
