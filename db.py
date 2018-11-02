import sqlite3
conn = sqlite3.connect('./data/data.db')

def init_db():
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS games(
      id TEXT UNIQUE NOT NULL,
      week TEXT,
      home_team TEXT,
      away_team TEXT,
      home_score INT,
      away_score INT,
      home_total_yards INT,
      home_rush_yards INT,
      home_pass_yards INT,
      home_1st_downs INT,
      home_turnovers INT,
      away_total_yards INT,
      away_rush_yards INT,
      away_pass_yards INT,
      away_1st_downs INT,
      away_turnovers INT,
      date TEXT
    );
    ''')
    conn.commit()

def save_season(season):
    c = conn.cursor()
    for s in season:
        try:
            c.execute(
                '''
      INSERT INTO games(
        id,
        week,
        home_team,
        away_team,
        home_score,
        away_score,
        home_total_yards,
        home_rush_yards,
        home_pass_yards,
        home_1st_downs,
        home_turnovers,
        away_total_yards,
        away_rush_yards,
        away_pass_yards,
        away_1st_downs,
        away_turnovers,
        date
      ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
      ''', (s['id'], s['week'], s['home_team'], s['away_team'],
            s['home_score'], s['away_score'], s['home_total_yards'],
            s['home_rush_yards'], s['home_pass_yards'], s['home_1st_downs'],
            s['home_turnovers'], s['away_total_yards'], s['away_rush_yards'],
            s['away_pass_yards'], s['away_1st_downs'], s['away_turnovers'],
            s['date']))
        except:
            print(f"Game already added: {s['id']}")

    conn.commit()
