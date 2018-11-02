import db
import time
import sys
from args import get_args
from season_requests import SeasonRequest, clean_team_name
from teams import teams

db.init_db()
args = get_args()
if args.start < 2005 or args.end > 2018:
    print("Invalid date range (must be 2005-2018")
    sys.exit(1)

last_request = time.time()
for year in range(args.start, args.end + 1):
    t = list(teams.values())
    total = db.get_games_by_season(year)
    if total == 268:
        print(f"Database complete for {year} season")
        continue
    for team in t:
        print(f'Pulling {clean_team_name(team)} / {year}')
        req = SeasonRequest(team, year)
        last_request = time.time()
        req.get_games()
        req.save_season()

        since = time.time() - last_request
        if since < args.rate:
            wait = args.rate - since
            print(f"Throttling requests for {'%.2f' % wait}s")
            time.sleep(wait)
