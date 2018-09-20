from apscheduler.schedulers.blocking import BlockingScheduler
from main import db
import price_gatherer as PG
import datetime

sched = BlockingScheduler()

current_league = "Delve"
current_league_HC = "Hardcore " + current_league

def add_unique(name, league, price, date):
	unique = Unique(name, league, price, date)
	db.session.add(unique)
	db.session.commit()

@sched.scheduled_job('interval', days = 1)
def timed_job():
	unique_names = open("uniqueNames.txt", "r", encoding = "latin-1").readlines()
	unique_names = list(map(lambda name : name.rstrip(), unique_names))

	prices = PG.gatherPrices(current_league)
	for unique, price in zip(unique_names, prices):
		add_unique(unique, current_league, price, datetime.date.today())

	prices = PG.gatherPrices(current_league_HC)
	for unique, price in zip(unique_names, prices):
		add_unique(unique, current_league_HC, price, datetime.date.today())

	db.session.commit()

sched.start()