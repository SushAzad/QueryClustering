from pymongo import MongoClient
import configparser

# reads the config file
config = configparser.ConfigParser()
config.read("config.ini")

# connects to mongo client
client = MongoClient(config.get("Database", "mongo"))

db = client.sample_airbnb

rev = db.listingsAndReviews.find_one()
print(rev)