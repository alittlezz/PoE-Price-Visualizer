from apscheduler.schedulers.blocking import BlockingScheduler
from main import db, Unique, add_unique
import datetime

sched = BlockingScheduler()

nr = 0

@sched.scheduled_job('interval', seconds = 30)
def timed_job():
	global nr
	add_unique("Test Item " + str(nr), "Breach HC", 123, datetime.date.today())
	nr += 1

sched.start()