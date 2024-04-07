from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import cumestatsteamgames, cumestatsteam, gamerotation, leaguegamefinder
import pandas as pd
import numpy as np
import json
import difflib
import time
import requests

gamefinder = leaguegamefinder.LeagueGameFinder()
games = gamefinder.get_data_frames()[0]
games = games[(games['SEASON_ID'].isin(['22023'])) & (games['GAME_ID'].str.startswith('00'))]
games['is_home'] = games['MATCHUP'].apply(lambda x: 1 if 'vs.' in x else 0)
home = games[games['is_home'] == 1][['GAME_ID', 'GAME_DATE', 'TEAM_ABBREVIATION', 'PTS']]
road = games[games['is_home'] == 0][['GAME_ID', 'GAME_DATE', 'TEAM_ABBREVIATION', 'PTS']]
merged = pd.merge(home, road, how='left', left_on=['GAME_ID'], right_on=['GAME_ID'])
merged = merged[['GAME_DATE_x', 'TEAM_ABBREVIATION_x', 'PTS_x', 'TEAM_ABBREVIATION_y', 'PTS_y']]
merged.columns = ['Date', 'Road', 'Road PTS', 'Home', 'Home PTS']
merged['Date'] = pd.to_datetime(merged['Date']).dt.tz_localize(None)
merged = merged.sort_values(by='Date').reset_index(drop=True)
merged.to_csv('updated_scores.csv', index=False)
