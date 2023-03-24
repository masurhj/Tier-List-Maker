
import hashlib
import json
import pyorient
import constants
import instructions



#if a db connection fails here, it should throw an exception
def orientCreateUser(inst):
    user = ({
        "username": inst["username"],
        "salt": inst["salt"],
        "hash": inst["hash"]
        })
    instructions.oclient.command("CREATE VERTEX USER CONTENT " + json.dumps(user))
    print("orient created user")

#need to delete the user and all of the tier lists they had created
def orientDeleteUser(inst):
    username = inst["username"]
    #delete all tierlists for the user
    #this one is a bit complex, need to test it
    instructions.oclient.command("DELETE VERTEX TIERLIST WHERE in.out[@Class = 'USER'].username='%s'" % (username))

    #delete the outgoing edges from the user
    #PRETTy SURE THIS IS UNNECESSARY
    #instructions.oclient.command("DELETE EDGE E WHERE @rid IN (SELECT out_ FROM USER WHERE username='%s')" % (username))

    #delete the user
    instructions.oclient.command("DELETE VERTEX USER WHERE username='%s'" % (username))

    print("orient deleted user")

def orientUpdateUser(inst):
    oldUsername = inst["oldUsername"]
    newUsername = inst["newUsername"]
    newSalt = inst["newSalt"]
    newHash = inst["newHash"]
    instructions.oclient.command("UPDATE USER SET username='%s', salt='%s', hash='%s' WHERE username='%s'" % (
        newUsername, newSalt, newHash, oldUsername))
    print("orient updated user")

def orientCreateTierList(inst):
    tierList = ({
        "title": inst["title"],
        "tiers": inst["tiers"]
        })
    res = instructions.oclient.command("CREATE VERTEX TIERLIST CONTENT " + json.dumps(tierList))
    instructions.oclient.command("CREATE EDGE FROM (SELECT FROM USER WHERE username='%s') TO (SELECT FROM TIERLIST WHERE @rid = '%s')" % (inst["username"], res[0]._rid))
    
    print("orient created tier list")

def orientUpdateTierList(inst):
    instructions.oclient.command("UPDATE TIERLIST SET title='%s', tiers=%s WHERE @RID IN (SELECT FROM (TRAVERSE * FROM (SELECT FROM USER WHERE username='%s'))) AND @class = 'TIERLIST' AND title='%s'"
            % (inst["newTitle"], inst["tiers"], inst["username"], inst["oldTitle"]))
    print("orient updated tier list")

def orientDeleteTierList(inst):
    username = inst["username"]
    title = inst["title"]
    instructions.oclient.command("DELETE VERTEX FROM (SELECT FROM (TRAVERSE * FROM (SELECT FROM USER WHERE username='%s')) WHERE @class='TIERLIST' AND title='%s')" % (username, title))
    print("orient deleted tier list")


