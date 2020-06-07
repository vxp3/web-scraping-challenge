from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time 
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mission_to_Mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission_to_Mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = Mission_to_Mars.scrape_all()
    mars.replace_one({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)