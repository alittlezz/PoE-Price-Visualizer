import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import pandas as pd

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ybosjhdyfhfhct:f2695864f05a7f9ceb35416bde81348b581cdf40f3cdad3d8cc915b8e97e029c@ec2-54-83-50-145.compute-1.amazonaws.com:5432/d59l2q0k6pnf1u"
db = SQLAlchemy(server)

monthToInt = {
	"Jan": 1,
	"Feb": 2,
	"March": 3,
	"April": 4,
	"May": 5,
	"June": 6,
	"July": 7,
	"Aug": 8,
	"Sep": 9,
	"Oct": 10,
	"Nov": 11,
	"Dec": 12
}

class Unique(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	league = db.Column(db.String(30))
	name = db.Column(db.String(35))
	price = db.Column(db.Float)
	date = db.Column(db.Date)	

	def __init__(self, name, league, price, date):
		self.name = name
		self.league = league
		self.price = price
		self.date = date

	def __repr__(self):
		return str(self.id) + ' ' + self.name + ' ' + self.league + ' ' + str(self.price) + ' ' + str(self.date)

	def __str__(self):
		return str(self.id) + ' ' + self.name + ' ' + self.league + ' ' + str(self.price) + ' ' + str(self.date)

def add_unique(name, league, price, date):
	unique = Unique(name, league, price, date)
	db.session.add(unique)
	#db.session.commit()

def get_uniques():
	results = db.session.query(Unique).all()
	for unique in results[-10:]:
		print(unique)

def delete_table():
	db.session.query(Unique).delete(synchronize_session=False)
	db.session.commit()

app = dash.Dash(__name__, server = server)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
    ])
)

def get_hc(csv_name):
	df = pd.read_csv(csv_name, encoding = "latin-1")
	unique_names = open("uniqueNames.txt", "r", encoding = "latin-1").readlines()
	unique_names = list(map(lambda name : name.rstrip(), unique_names))
	for row in df.iterrows():
		day = int(row[1][0].split()[0])
		if day < 19:
			continue
		month = monthToInt[row[1][0].split()[1]]
		date = datetime.date(2018, month, day)
		for unique, price in zip(unique_names, row[1][1:]):
			add_unique(unique, "Delve Hardcore", price, date)
	db.session.commit()
	#os.system("shutdown -s -t 0")

if __name__ == "__main__":
	#add_unique("Tudor eat", "HH NO QQ", 123.23, datetime.date.today())
	get_uniques()
	app.run_server(debug=False)