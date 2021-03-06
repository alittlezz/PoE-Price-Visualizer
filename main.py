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
server.config["SQLALCHEMY_DATABASE_URI"] = "private_uri"
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

def get_timeline(unique_name, league_name):
	prices = get_prices(unique_name, league_name)
	dates = get_dates_range(datetime.date(2018, 9, 1), datetime.date.today())
	dates_to_delete = []
	for price, date in zip(prices, dates):
		if price == -1:
			dates_to_delete.append(date)
	for date in dates_to_delete:
		dates.remove(date)
	prices = list(filter(lambda x : x > 0, prices))
	return (dates, prices)

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
		df_sc = get_timeline(input_data, "Delve")
		df_hc = get_timeline(input_data, "Hardcore Delve")
		return dcc.Graph(
	    	id = "graph_1",
			figure = {
			"data" : [
				{'x' : df_sc[0], 
				 'y' : df_sc[1], 
				 "type" : "line", 
				 "name" : league_name},
				{'x' : df_hc[0],
				 'y' : df_hc[1],
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

if __name__ == '__main__':
	app.run_server(debug=False)