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

league_name = "Delve"

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ybosjhdyfhfhct:f2695864f05a7f9ceb35416bde81348b581cdf40f3cdad3d8cc915b8e97e029c@ec2-54-83-50-145.compute-1.amazonaws.com:5432/d59l2q0k6pnf1u"
app = dash.Dash(server = server)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
db = SQLAlchemy(server)

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
		return self.name + ' ' + self.league + ' ' + str(self.price) + ' ' + str(self.date)

	def __str__(self):
		return self.name + ' ' + self.league + ' ' + str(self.price) + ' ' + str(self.date)

def get_prices(name, league):
	query = Unique.query.with_entities(Unique.price).filter(Unique.name == name, Unique.league == league).all()
	return [price[0] for price in query]

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
		app.run_server(debug=False)