
import redis
from pymongo import MongoClient
import pyorient
global mClient, oClient, userDB, tierlistDB, mConnected, oConnected, rClient
mConnected = False
oConnected = False
rConnected = False

#only need one database and the redis queue connection
def connectionsAreValid():
    global oConnected, mConnected, rConnected
    return (oConnected or mConnected) and rConnected

def tryConnections():
    global mClient, oClient, mConnected, oConnected, userDB, tierlistDB, rConnected, rClient

    #it's okay to have just one connection. Only need to reconnect if current connections fail
    if (connectionsAreValid()):
        return True
    if (not mConnected):
        try:
            mClient = MongoClient("433-11.csse.rose-hulman.edu", 40000, serverSelectionTimeoutMS=1000)
            dbname = mClient['tierList']
            userDB = dbname["users"]
            tierlistDB = dbname["tierlists"]
            mClient.server_info()
            print("Connected to Mongo Client")
            mConnected = True
        except:
            mConnected = False
            print("Failed to connect to Mongo Client")
    if (not oConnected):
        try:
            oClient = pyorient.OrientDB("433-12.csse.rose-hulman.edu", 2424)
            oClient.connect("root", "ich3aeNg")
            oClient.db_open("TierList", "admin", "admin")
            oConnected = True
            print("Connected to Orient Client")
        except:
            oConnected = False
            print("Failed to connect to Orient Client")
    if (not rConnected):
        try:
            rClient = redis.Redis(host="433-13.csse.rose-hulman.edu", port=6379)
            rClient.ping()
            rConnected = True
            print("Connected to Redis Client")
        except:
            rConnected = False
            print("Failed to connect to Redis Client")

    return connectionsAreValid()