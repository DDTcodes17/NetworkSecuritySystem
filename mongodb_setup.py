
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

SAFE_PASSWORD = urllib.parse.quote_plus("MONGODBdt2002$")
uri = f"mongodb+srv://DevDhruv:{SAFE_PASSWORD}@cluster0.5i5secp.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)