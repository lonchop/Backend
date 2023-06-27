from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local

# Base de datos remota
# url = "mongodb+srv://backend:DnBicYSBA5gCgd5m@cluster0.4o4pk5m.mongodb.net/?retryWrites=true&w=majority"

db_client = MongoClient("mongodb+srv://backend:DnBicYSBA5gCgd5m@cluster0.4o4pk5m.mongodb.net/?retryWrites=true&w=majority").backend
