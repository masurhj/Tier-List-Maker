
import mongo_ops
import orient_ops
import constants
import pyorient
import pymongo
from pymongo import MongoClient
import schema_check

mongoConnected = False
orientConnected = False
oclient = None
mclient = None

def establishConnections():
    global mongoConnected
    global orientConnected
    global oclient
    global mclient
    if (not mongoConnected):
        try:
            mclient = MongoClient(constants.MONGO_VM, constants.MONGO_PORT, serverSelectionTimeoutMS=100)
            val = mclient.server_info()
            mongoConnected = True
        except:
            mongoConnected = False
    if (not orientConnected):
        try:
            oclient = pyorient.OrientDB(constants.ORIENT_VM, constants.ORIENT_PORT)
            oclient.connect(constants.ORIENT_USERNAME, constants.ORIENT_PASSWORD)
            oclient.db_open(constants.ORIENT_DB_NAME, constants.ORIENT_DB_USERNAME, constants.ORIENT_DB_PASSWORD)
            orientConnected = True
        except:
            orientConnected = False

def runInstruction(jsonInst, mongoOrOrient):
    global mongoConnected
    global orientConnected
    global oclient
    global moclient
    establishConnections()
    if (jsonInst is None):
        return False
    #small optimization:
    if ((mongoOrOrient == constants.ORIENT_KEY and not orientConnected) or
            mongoOrOrient == constants.MONGO_KEY and not mongoConnected):
        return False
    inst = jsonInst['instruction']
    success = False
    try:
        if (inst == constants.CREATE_USER and schema_check.createUser(jsonInst)):
            if (mongoOrOrient == constants.ORIENT_KEY):
                orient_ops.orientCreateUser(jsonInst)
            else:
                mongo_ops.mongoCreateUser(jsonInst)
        elif (inst == constants.DELETE_USER and schema_check.deleteUser(jsonInst)):
            if (mongoOrOrient == constants.ORIENT_KEY):
                orient_ops.orientDeleteUser(jsonInst)
            else:
                mongo_ops.mongoDeleteUser(jsonInst)
        elif (inst == constants.UPDATE_USER and schema_check.updateUser(jsonInst)):
            if (mongoOrOrient == constants.ORIENT_KEY):
                orient_ops.orientUpdateUser(jsonInst)
            else:
                mongo_ops.mongoUpdateUser(jsonInst)
        elif (inst == constants.CREATE_TIERLIST and schema_check.createTierList(jsonInst)):
            if (mongoOrOrient == constants.ORIENT_KEY):
                orient_ops.orientCreateTierList(jsonInst)
            else:
                mongo_ops.mongoCreateTierList(jsonInst)
        elif (inst == constants.UPDATE_TIERLIST and schema_check.updateTierList(jsonInst)):
            if (mongoOrOrient == constants.ORIENT_KEY):
                orient_ops.orientUpdateTierList(jsonInst)
            else:
                mongo_ops.mongoUpdateTierList(jsonInst)
        elif (inst == constants.DELETE_TIERLIST and schema_check.deleteTierList(jsonInst)):
            if (mongoOrOrient == constants.ORIENT_KEY):
                orient_ops.orientDeleteTierList(jsonInst)
            else:
                mongo_ops.mongoDeleteTierList(jsonInst)
        else:
            print("unsupported instruction received")
            #throw an error here
        success = True
    except:
        success = False

    if (not success):
        if (mongoOrOrient == constants.ORIENT_KEY):
            orientConnected = False
        elif (mongoOrOrient == constants.MONGO_KEY):
            mongoConnected = False
    return success



