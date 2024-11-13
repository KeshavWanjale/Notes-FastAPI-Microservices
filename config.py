from pymongo import MongoClient


client = MongoClient("mongodb+srv://admin:admin123@cluster0.gtldf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.user_db

user_collection = db["user_data"]

notes_collection = db["notes_data"]