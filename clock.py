from apscheduler.schedulers.blocking import BlockingScheduler
from main import db, add_price
import sys
sys.path.append("/price_gatherer")
from gatherer import price_gatherer as PG
import datetime

sched = BlockingScheduler()

current_league = "Delve"
current_league_HC = "Hardcore " + current_league

@sched.scheduled_job('interval', hours = 1, misfire_grace_time = None)
def timed_job():
	unique_names = open("uniqueNames.txt", "r", encoding = "latin-1").readlines()
	unique_names = list(map(lambda name : name.rstrip(), unique_names))

	prices = PG.gatherPrices(current_league)
	print("Prices gathered")
	for unique, price in zip(unique_names, prices):
		add_price(unique, current_league, price)

	prices = PG.gatherPrices(current_league_HC)
	print("Prices gathered HC")
	for unique, price in zip(unique_names, prices):
		add_price(unique, current_league_HC, price)

	db.session.commit()

sched.start()