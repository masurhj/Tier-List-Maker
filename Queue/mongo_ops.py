
import pymongo
from pymongo import MongoClient
import constants
import instructions


def mongoCreateUser(inst):
    users = instructions.mclient.tierList.users
    users.insert_one({'username': inst["username"], 'salt': inst["salt"], 'hash': inst["hash"]})
    print("mongo created user")

def mongoDeleteUser(inst):
    users = instructions.mclient['tierList'].users
    tierlists = instructions.mclient['tierList'].tierlists
    #delet all of their tier lists
    tierlists.delete_many({"username": inst["username"]})
    #delete the user
    users.delete_one({"username": inst["username"]})
    print("mongo deleted user")

def mongoUpdateUser(inst):
    users = instructions.mclient['tierList'].users
    users.update_one({"username": inst["oldUsername"]}, {"$set": {"username": inst["newUsername"], "salt": inst["newSalt"], "hash": inst["newHash"]}})
    print("mongo updated user")

def mongoCreateTierList(inst):
    tierlists = instructions.mclient['tierList'].tierlists
    users = instructions.mclient['tierList'].users

    li = tierlists.insert_one({"title": inst["title"], "tiers": inst["tiers"]})
    #add the id of the new tier list to the list of tierlists created by the user
    res = users.update_one({"username": inst["username"]}, {"$push": {"tierlist-ids": li.inserted_id}})
    if (res.modified_count < 1):
        print("ERROR: failed to find user with username: " + inst["username"])
    print("mongo create tier list")

def mongoUpdateTierList(inst):
    tierlists = instructions.mclient['tierList'].tierlists
    users = instructions.mclient['tierList'].users
    tierlist_ids = users.find_one({"username": inst["username"]}).get("tierlist-ids")
    if (tierlist_ids is None or len(tierlist_ids) < 1):
        print("no tierlists found for username: " + inst["username"])
    tierlists.update_one({"title": inst["oldTitle"], "_id": {"$in": tierlist_ids}}, {"$set": {"title": inst["newTitle"], "tiers": inst["tiers"]}})

    print("mongo update tier list")

def mongoDeleteTierList(inst):
    tierlists = instructions.mclient['tierList'].tierlists
    users = instructions.mclient['tierList'].users
    tierlist_ids = users.find_one({"username": inst["username"]}).get("tierlist-ids")
    res = tierlists.find_one({"title": inst["title"], "_id": {"$in": tierlist_ids}})
    if (res is None):
        print("ERROR user does not own tierlist with title")
        return
    tid = res.get("_id")
    users.update_one({"username": inst["username"]}, {"$pull": {"tierlist-ids": tid}})
    tierlists.delete_one({"title": inst["title"], "_id": {"$in": tierlist_ids}})


    print("mongo delete tier list")


