import json
import connections


def pushToRedisQueue(doc):
    s = json.dumps(doc)
    connections.rClient.rpush("orient", s)
    connections.rClient.rpush("mongo", s)

def createUser(username, salt, _hash):
    global rClient, currentUser
    doc = ({
        "instruction": "createUser",
        "username": username,
        "salt": salt.decode("utf-8"),
        "hash": _hash.decode("utf-8")
        })
    print(doc)
    json.dumps(doc)
    pushToRedisQueue(doc)
    return True

def deleteUser(username):
    doc = ({
        "instruction": "deleteUser",
        "username": username
        })
    print(doc)

    pushToRedisQueue(doc)
    return True

def updateUser(oldUsername, newUsername, newSalt, newHash):
    global currentUser
    doc = ({
        "instruction": "updateUser",
        "oldUsername": oldUsername,
        "newUsername": newUsername,
        "newSalt": newSalt.decode('utf-8'),
        "newHash": newHash.decode('utf-8')
        })
    print(doc)
    pushToRedisQueue(doc)
    currentUser = newUsername

    return True

def createTierList(currentUser, title, l1, t1, l2, t2, l3, t3):
    t1List = t1.split(',')
    t2List = t2.split(',')
    t3List = t3.split(',')

    doc = ({
        "instruction": "createTierList",
        "title": title,
        "username": currentUser,
        "tiers": [{
            "label1": [{
                "name": l1,
                "values": t1List
            }],
            "label2": [{
                "name": l2,
                "values": t2List
            }],
            "label3": [{
                "name": l3,
                "values": t3List
            }]
        }]
        })

    print(doc)
    pushToRedisQueue(doc)
    return True


def updateTierList(currentUser, oldTitle, newTitle, l1, t1, l2, t2, l3, t3):
    t1List = t1.split(',')
    t2List = t2.split(',')
    t3List = t3.split(',')

    doc = ({
        "instruction": "updateTierList",
        "oldTitle": oldTitle,
        "newTitle": newTitle,
        "username": currentUser,
        "tiers": [{
            "label1": [{
                "name": l1,
                "values": t1List
            }],
            "label2": [{
                "name": l2,
                "values": t2List
            }],
            "label3": [{
                "name": l3,
                "values": t3List
            }]
        }]
        })
    pushToRedisQueue(doc)
    return True

def deleteTierList(currentUser, title):
    doc = ({
        "instruction": "deleteTierList",
        "username": currentUser,
        "title": title
    })
    pushToRedisQueue(doc)
    return True