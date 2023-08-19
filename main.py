import requests
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)

# MongoDB setup
connection_string = "mongodb://localhost:27017/"
database_name = "group10project"
collection_name = "marketdata"

client = MongoClient(connection_string)
database = client[database_name]
collection = database[collection_name]

@app.route('/')
def index():

    # Rapid API call to fetch nifty 50 data
    api_key = "477e94f704msh441ca080f0241b0p1e65cbjsn010486417e81"
    url = "https://latest-stock-price.p.rapidapi.com/price"
    query_params = {
        "Indices": "NIFTY 50"
    }
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com"
    }

    response = requests.get(url, params=query_params, headers=headers)

    if response.status_code == 200:
        api_data = response.json()
        stock_data_list = api_data

        # Clear previous data
        collection.delete_many({})

        # Inserting data to MongoDB
        if stock_data_list:
            collection.insert_many(stock_data_list)

        return render_template('index.html', stock_data=stock_data_list)
    else:
        return "API Error: " + str(response.status_code)

@app.route('/line-chart')
def line_chart():
    return render_template('line_chart.html', stock_data=collection.find({}),)

@app.route('/barchart')
def bar_chart():
    return render_template('bar_chart.html', stock_data=collection.find({}))

@app.route('/pie-chart')
def pie_chart():
    return render_template('pie_chart.html', stock_data=collection.find({}))





if __name__ == "__main__":
    app.run(debug=True)












