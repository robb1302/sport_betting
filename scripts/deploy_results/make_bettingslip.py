def find_and_append_module_path():
    import sys
    import os
    current_directory = os.getcwd()
    substring_to_find = 'sport_betting'
    index = current_directory.find(substring_to_find)
    
    if index != -1:
        parent_dir = os.path.join(current_directory[:index], substring_to_find)
        sys.path.append(parent_dir)
find_and_append_module_path()


import config as CONFIG
import pandas as pd

def main(results,fixtures):

    # Merge dataframes
    df = results.merge(fixtures, left_on=['Home Team', 'Div'], right_on=['HomeTeam', 'Div'], how='inner')[
        ['Div', 'Home Team', 'Away Team', 'Home Prob', 'Away Prob', 'Draw Prob', 'AvgH', 'AvgD', 'AvgA',
         'Fair Home Odd', 'Fair Draw Odd', 'Fair Away Odd']]

    # Calculate additional columns
    df['AvgH/Fair Home Odd'] = df['AvgH'] / df['Fair Home Odd']
    df['AvgD/Fair Draw Odd'] = df['AvgD'] / df['Fair Draw Odd']
    df['AvgA/Fair Away Odd'] = df['AvgA'] / df['Fair Away Odd']

    # Filter data
    potential_away_bets = (df['AvgA/Fair Away Odd'] > 1) & (df["Away Prob"] > 0.45)
    df_away = df[potential_away_bets]

    potential_home_bets = (df['AvgH/Fair Home Odd'] > 1) & (df["Home Prob"] > 0.45)
    df_home = df[potential_home_bets]

    # Create copies of df_away and df_home to avoid the SettingWithCopyWarning
    df_away = df_away.copy()
    df_home = df_home.copy()

    # Modify the copied dataframes
    df_away['potential'] = df['AvgA/Fair Away Odd']
    df_away["bet on"] = "away"

    df_home['potential'] = df_home['AvgH/Fair Home Odd']
    df_home["bet on"] = "home"

    # Concatenate the modified dataframes
    betting_slip = pd.concat([df_away, df_home], axis=0)[["Div", "Home Team", "Away Team", "bet on", "potential"]]
    betting_slip = betting_slip.dropna()
    # Sort the betting slip by 'potential' in descending order
    betting_slip = betting_slip.sort_values('potential', ascending=False)

    return betting_slip

if __name__ == "__main__":
    
    # Read data from CSV file
    print()
    print("####BETTING SLIP#####")
    print("read results and fixtures...")
    results = pd.read_csv(f"{CONFIG.DATA_FOLDER_RESULTS}results.csv", index_col=0)
    fixtures = pd.read_csv(f"{CONFIG.DATA_FOLDER_FIXTURES}update.csv", index_col=0)

    print("make betting slips...")
    betting_slip = main(results,fixtures)

    print("save data...")
    betting_slip.to_csv(f"{CONFIG.DATA_FOLDER_RESULTS}betting_slip.csv",index=False)
    print("sucessfully created betting slip.")