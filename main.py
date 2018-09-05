import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

league_name = "Delve"

server = Flask(__name__)
app = dash.Dash(server = server)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.read_csv("Unique Data.csv")
dfHC = pd.read_csv("Unique Data HC.csv")
headers = list(df.columns.values)

unique_names = open("uniqueNames.txt", "r").readlines()
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

	    html.Div(children='A web application for viewing the price changes of uniques', 
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


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update(input_data):
	if input_data in headers:
		return dcc.Graph(
	    	id = "graph_1",
			figure = {
			"data" : [
				{'x' : df["Date"], 
				 'y' : df[input_data], 
				 "type" : "line", 
				 "name" : league_name},
				{'x' : dfHC["Date"],
				 'y' : dfHC[input_data],
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
    app.run_server(debug=True)