import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:SlJAFTBO@localhost/Path_of_Exile_Visualizer_DB"
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

def add_unique(name, league, price, date):
	unique = Unique(name, league, price, date)
	db.session.add(unique)
	db.session.commit()

app = dash.Dash(__name__, server = server)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text')
    ])
)

if __name__ == "__main__":
	app.run_server(debug=True)