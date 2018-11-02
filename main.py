import db
import time
import sys
from args import get_args
from season_requests import SeasonRequest
from teams import teams

REQUEST_RATE = 2  # minimum seconds between requests

db.init_db()
args = get_args()
if args.start < 2005 or args.end > 2018:
    print("Invalid date range (must be 2005-2018")
    sys.exit(1)

last_request = time.time()
for year in range(args.start, args.end + 1):
    for team in list(teams.values()):
        print(f'Pulling {team} / {year}')
        req = SeasonRequest(team, year)
        last_request = time.time()
        req.get_games()
        req.save_season()
        since = time.time() - last_request
        if since < args.rate:
            wait = args.rate - since
            print(f"Throttling requests for {'%.2f' % wait}s")
            time.sleep(wait)
