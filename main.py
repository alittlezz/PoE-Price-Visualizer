import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import numpy as np
import random
import sys

league_name = "Delve"

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jrpvletsmdcqow:a2927f5c870c6efe8427e8709469eab75830a9c8898486c292e1536550d20fa1@ec2-23-23-253-106.compute-1.amazonaws.com:5432/d6178vkpqi46i8"
app = dash.Dash(server = server)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
db = SQLAlchemy(server)

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

def get_prices(name, league):
	query = Unique.query.filter(Unique.name == name, Unique.league == league).first()
	return list(query.prices)

def add_price(name, league, price):
	unique = db.session.query(Unique).filter(Unique.name == name, Unique.league == league)
	new_prices = unique.first().prices + [price]
	unique.update({"prices" : new_prices})

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
		#print("Finished " + unique)
	#os.system("shutdown -s -t 0")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

unique_names = open("uniqueNames.txt", "r", encoding = "latin-1").readlines()
unique_names = list(map(lambda name : name.rstrip(), unique_names))

app.layout = html.Div(
	style={'backgroundColor': colors['background'], "height" : "100vh"}, 
	children=[
	    html.H1(
	        children='Unique price viewer',
	        style={
	            'textAlign': 'center',
	            'color': colors['text']
	        }
	    ),

	    html.Div(id = "title",
	    		 children="Meme title", 
	    		 style={
			        'textAlign': 'center',
			        'color': colors['text']
	    		}
	    ),
	    html.Div(
		    children = dcc.Dropdown(id = "input",
		    			 options = [
		    			 	{"label" : name, "value" : name} for name in unique_names
		    			 ],
		    			 placeholder = "Select unique"
		   			   ),
		    style = {
		    	"width" : "25vw"
		    }
	    ),

	    html.Div(id = "output-graph")
	]
)

def get_dates_range(start, end):
	return [start + datetime.timedelta(days = i) for i in range(0, (end - start).days + 1)]

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update(input_data):
	if input_data in unique_names:
		df_sc = get_prices(input_data, "Delve")
		df_hc = get_prices(input_data, "Hardcore Delve")
		dates = get_dates_range(datetime.date(2018, 9, 1), datetime.date.today())
		return dcc.Graph(
	    	id = "graph_1",
			figure = {
			"data" : [
				{'x' : dates, 
				 'y' : df_sc, 
				 "type" : "line", 
				 "name" : league_name},
				{'x' : dates,
				 'y' : df_hc,
				 "type" : "line",
				 "name" : league_name + " Hardcore"}
			],
			'layout': {
				"title" : input_data,
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                "yaxis" : {
                	"title" : "Chaos orbs"
                }
            }
		})
	# else:
	# 	return html.Div(
	# 		id = "graph_1",
	# 		style = {
	# 			"color" : colors["background"],
	# 			"height" : "500px"
	# 		}
	# 	)

if __name__ == '__main__':
	init_database()
	app.run_server(debug=False)