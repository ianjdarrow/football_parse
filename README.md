# football_scraper

### a library to save scott from having to learn to parse HTML

## installation

- clone this repo
- `pipenv shell` and `pipenv install`
- if you don't want to use pipenv, the dependencies are just `requests` and `bs4`

## usage

- `python main.py` will pull down NFL stats from the current year and save them to a sqlite database. see `db.py` for the very simple schema.
- you can optionally pass `--start {year}` or `--end {year}`to pull a range. both default to the current year.
- by default, the library ensures a minimum of two seconds between API requests. you can change this by passing `--rate {seconds}`, where `seconds` is the new minimum delay.

## license

apache-2
