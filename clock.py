from apscheduler.schedulers.blocking import BlockingScheduler
from main import db, add_unique
import price_gatherer as PG
import datetime

sched = BlockingScheduler()

current_league = "Delve"

@sched.scheduled_job('interval', days = 1)
def timed_job():
	unique_names = open("uniqueNames.txt", "r", encoding = "latin-1").readlines()
	unique_names = list(map(lambda name : name.rstrip(), unique_names))

	prices = PG.gatherPrices(current_league)
	for unique, price in zip(unique_names, prices):
		add_unique(unique, current_league, price, datetime.date.today())

	prices = PG.gatherPrices("Hardcore " + current_league)
	for unique, price in zip(unique_names, prices):
		add_unique(unique, current_league + " Hardcore", price, datetime.date.today())

	db.session.commit()

sched.start()