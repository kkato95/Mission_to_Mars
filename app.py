from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Flask setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# Tells python our app will connect to Mongo using URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# URI we'll be using to connect our app to Mongo
mongo = PyMongo(app)

# Create app route to reach HTML page
@app.route("/")
def index():
    # Find mars collection in database
    # Assign path to mars variable
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Createing the route for scraping - button of the web application
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()