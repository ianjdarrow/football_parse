import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

from teams import teams, keys
from db import save_season

def format_date(date, year, time):
    return datetime.strptime(f'{date}, {year} {time.split(" ")[0]}',
                             "%B %d, %Y %I:%M%p")

def clean_team_name(team_name):
    if team_name == 'CRD':
        return 'ARI'
    if team_name == 'RAV':
        return 'BAL'
    if team_name == 'GNB':
        return 'GB'
    if team_name == 'HTX':
        return 'HOU'
    if team_name == 'CLT':
        return 'IND'
    if team_name == 'NWE':
        return 'NE'
    if team_name == 'NOR':
        return 'NO'
    if team_name == 'RAI':
        return 'OAK'
    if team_name == 'SDG':
        return 'LAC'
    if team_name == 'RAM':
        return 'LAR'
    if team_name == 'SFO':
        return 'SF'
    if team_name == 'TAM':
        return 'TB'
    if team_name == 'OTI':
        return 'TEN'
    return team_name

class SeasonRequest:
    def __init__(self, team, year):
        self.team = team
        self.year = year
        self.results = []

    def get_games(self):
        url = f'https://www.pro-football-reference.com/teams/{self.team.lower()}/{self.year}.htm'
        page = requests.get(url)
        parsed = bs(page.content, 'html.parser')
        games_table = parsed.find(id='games')
        games = games_table.select('tr')
        lines = [g.select('th, td') for g in games]

        results = []
        for line in lines[2:]:
            data = [l.get_text() for l in line]
            obj = dict(zip(keys, data[:len(keys)]))
            # game hasn't happened yet
            if obj['win_loss'] == "":
                continue
            del obj[""]
            del obj["rec"]
            is_home = obj['away'] == ''
            date = format_date(obj["date"], self.year, obj["time"])

            result = {
                "week":
                obj['week'],
                "home_team":
                self.team if is_home else teams[obj['opponent']],
                "away_team":
                self.team if not is_home else teams[obj['opponent']],
                "home_score":
                obj['team_score'] if is_home else obj['opponent_score'],
                "away_score":
                obj['team_score'] if not is_home else obj['opponent_score'],
                "home_total_yards":
                obj['team_total_yards'] if is_home else obj['opp_total_yards'],
                "home_rush_yards":
                obj['team_rush_yards'] if is_home else obj['opp_rush_yards'],
                "home_pass_yards":
                obj['team_pass_yards'] if is_home else obj['opp_pass_yards'],
                "home_turnovers":
                obj['team_turnovers'] if is_home else obj['opp_turnovers'],
                "home_1st_downs":
                obj['team_1st_downs'] if is_home else obj['opp_1st_downs'],
                "away_total_yards":
                obj['team_total_yards']
                if not is_home else obj['opp_total_yards'],
                "away_rush_yards":
                obj['team_rush_yards']
                if not is_home else obj['opp_rush_yards'],
                "away_pass_yards":
                obj['team_pass_yards']
                if not is_home else obj['opp_pass_yards'],
                "away_turnovers":
                obj['team_turnovers'] if not is_home else obj['opp_turnovers'],
                "away_1st_downs":
                obj['team_1st_downs'] if not is_home else obj['opp_1st_downs'],
                "date":
                str(date),
            }
            result['home_team'] = clean_team_name(result['home_team'])
            result['away_team'] = clean_team_name(result['away_team'])
            result[
                'id'] = f'{self.year}-{result["week"]}-{result["home_team"]}-{result["away_team"]}'

            results.append(result)

        self.results = results

    def save_season(self):
        save_season(self.results)
        print(f"Saved season: {clean_team_name(self.team)} / {self.year}")
