from flask import Flask
from flask import request
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
import os

MONGO_HOST= 'mongodb://127.0.0.1:27017/twitterdb'  # assuming you have mongoDB installed locally
                                             # and a database called 'twitterdb'
app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/api/tweets")
def tweets():
    #setup the connection to the gauges database
    client = MongoClient(MONGO_HOST)
    db = client.twitterdb

    #query the DB for all the gaugepoints
    result = db.twitter_data.find()

    #Now turn the results into valid JSON
    return str(json.dumps({'type': "FeatureCollection" ,'features':list(result)},default=json_util.default))


@app.route("/api/tweets/param")
def param():
    #setup the connection to the gauges database
    client = MongoClient(MONGO_HOST)
    db = client.twitterdb

     #get the request parameters
    
    state = str(request.args.get('option_state'))
    marker1 = str(request.args.get('param1'))
    marker2 = str(request.args.get('param2'))
    marker3 = str(request.args.get('param3'))

    if marker1 == 'None' and marker2 == 'None' and marker3 == 'None':
    	if state == 'all':
    		result = db.twitter_data.find()
    	else:
    		result = db.twitter_data.find({
    			"address.key_state": state
    		})   		
    	pass
    else:
    	if state == 'all':
    		print (state+" "+marker1+" "+marker2+" "+marker3)
    		query = { 
    			"properties_text.sentiment": {"$in": [marker1, marker2, marker3]} 
    			}
    		print (query)
    		result = db.twitter_data.find(query)
    	else:
    		query = {
    			"properties_text.sentiment": {"$in": [marker1, marker2, marker3]},
    			"address.key_state": state
    		} 
    		result = db.twitter_data.find(query)
    		print (query) 
    
    #Now turn the results into valid JSON
    return str(json.dumps({'type': "FeatureCollection" ,'features':list(result)},default=json_util.default))

@app.route("/api/tweets/data_graphics")
def data_graphics():
    #setup the connection to the gauges database
    client = MongoClient(MONGO_HOST)
    db = client.twitterdb

    positiveCDMX = db.twitter_data.count({ "address.key_state": 'CDMX', "properties_text.sentiment": "positive"})
    negativeCDMX = db.twitter_data.count({ "address.key_state": 'CDMX', "properties_text.sentiment": "negative"})
    neutralCDMX = db.twitter_data.count({ "address.key_state": 'CDMX', "properties_text.sentiment": "neutral"})

    positiveJal = db.twitter_data.count({ "address.key_state": 'Jalisco', "properties_text.sentiment": "positive"})
    negativeJal = db.twitter_data.count({ "address.key_state": 'Jalisco', "properties_text.sentiment": "negative"})
    neutralJal = db.twitter_data.count({ "address.key_state": 'Jalisco', "properties_text.sentiment": "neutral"})

    positiveQuin = db.twitter_data.count({ "address.key_state": 'Quintanaroo', "properties_text.sentiment": "positive"})
    negativeQuin = db.twitter_data.count({ "address.key_state": 'Quintanaroo', "properties_text.sentiment": "negative"})
    neutralQuin = db.twitter_data.count({ "address.key_state": 'Quintanaroo', "properties_text.sentiment": "neutral"})

    positiveNuev = db.twitter_data.count({ "address.key_state": 'NuevoLeon', "properties_text.sentiment": "positive"})
    negativeNuev = db.twitter_data.count({ "address.key_state": 'NuevoLeon', "properties_text.sentiment": "negative"})
    neutralNuev = db.twitter_data.count({ "address.key_state": 'NuevoLeon', "properties_text.sentiment": "neutral"})

    positiveGue = db.twitter_data.count({ "address.key_state": 'Guerrero', "properties_text.sentiment": "positive"})
    negativeGue = db.twitter_data.count({ "address.key_state": 'Guerrero', "properties_text.sentiment": "negative"})
    neutralGue = db.twitter_data.count({ "address.key_state": 'Guerrero', "properties_text.sentiment": "neutral"})  		
    
    format_data = {
    	  'cols': [
    	  		{'label': 'Estados', 'type': 'string'},
    	 		{'label': 'positive', 'type': 'number'},
    	 		{'label': 'neutral', 'type': 'number'},
		        {'label': 'negative', 'type': 'number'}		  
		        ],
		  'rows': [
		  	{"c":[{"v":"CDMX"},{"v":positiveCDMX}, {"v":neutralCDMX}, {"v":negativeCDMX}]},
	        {"c":[{"v":"Jalisco"},{"v":positiveJal}, {"v":neutralJal}, {"v":negativeJal}]},
	        {"c":[{"v":"Quintanaroo"},{"v":positiveQuin}, {"v":neutralQuin}, {"v":negativeQuin}]},
	        {"c":[{"v":"NuevoLeon"},{"v":positiveNuev}, {"v":neutralNuev}, {"v":negativeNuev}]},
	        {"c":[{"v":"Guerrero"},{"v":positiveGue}, {"v":neutralGue}, {"v":negativeGue}]}

           ]
		  
    }

    #Now turn the results into valid JSON
    return str(json.dumps(format_data,default=json_util.default))


@app.route("/index")
@app.route("/")
def index():
    return render_template("map.html")



if __name__ == '__main__':
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)