import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import pandas as pd
import time


server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jrpvletsmdcqow:a2927f5c870c6efe8427e8709469eab75830a9c8898486c292e1536550d20fa1@ec2-23-23-253-106.compute-1.amazonaws.com:5432/d6178vkpqi46i8"
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
	prices = db.Column(db.ARRAY(db.FLOAT))	

	def __init__(self, name, league):
		self.name = name
		self.league = league
		self.prices = []

	def __repr__(self):
		return str(self.id) + ' ' + self.name + ' ' + self.league + ' ' + str(self.prices)

	def __str__(self):
		return str(self.id) + ' ' + self.name + ' ' + self.league + ' ' + str(self.prices)

def testing():
	prices = price_gatherer.gatherPrices("Delve")

def add_unique(name, league):
	unique = Unique(name, league)
	db.session.add(unique)
	#db.session.commit()

def add_price(name, league, price):
	unique = db.session.query(Unique).filter(Unique.name == name, Unique.league == league)
	new_prices = unique.first().prices + [price]
	unique.update({"prices" : new_prices})

def get_uniques():
	results = db.session.query(Unique).all()
	for unique in results[-50:]:
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

def init_database():
	df = pd.read_csv("Unique Data.csv", encoding = "latin-1")
	dfHC = pd.read_csv("Unique Data HC.csv", encoding = "latin-1")
	unique_names = open("uniqueNames.txt", "r", encoding = "latin-1").readlines()
	unique_names = list(map(lambda name : name.rstrip(), unique_names))
	# for unique in unique_names:
	# 	add_unique(unique, "Delve")
	# 	add_unique(unique, "Hardcore Delve")
	# db.session.commit()
	for unique in unique_names:
		for pc, pcHC in zip(df[unique][22:], dfHC[unique][22:]):
			pc = int(pc * 100) / 100
			pcHC = int(pcHC * 100) / 100
			add_price(unique, "Delve", pc)
			add_price(unique, "Hardcore Delve", pcHC)
		db.session.commit()
		print("Finished " + unique)
	#os.system("shutdown -s -t 0")

if __name__ == "__main__":
	#add_unique("Tudor eat", "HH NO QQ", 123.23, datetime.date.today())
	#get_uniques()
	app.run_server(debug=False)