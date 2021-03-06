import argparse
from datetime import datetime

def get_args():
    year = datetime.now().year
    parser = argparse.ArgumentParser(
        description='Pull NFL stats into a database')
    parser.add_argument(
        '--start',
        type=int,
        default=year,
        dest="start",
        help='year to start (default current year)')
    parser.add_argument(
        '--end',
        type=int,
        default=year,
        dest="end",
        help='year to end (default current year')
    parser.add_argument(
        '--rate',
        type=float,
        default=3.0,
        dest="rate",
        help='seconds per API request')
    parser.add_argument(
        '--force-update',
        dest="force",
        action='store_true',
        help='delete existing database entries within range and repopulate')
    return parser.parse_args()
