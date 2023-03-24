
def createUser(jsonInst):
    try:
        jsonInst["username"]
        jsonInst["salt"]
        jsonInst["hash"]
        return True
    except:
        print("required field for createUser: username, salt, hash")
        return False

def deleteUser(jsonInst):
    try:
        jsonInst["username"]
        return True
    except:
        print("required field for deleteUser: username")
        return False


def updateUser(jsonInst):
    try:
        jsonInst["oldUsername"]
        jsonInst["newUsername"]
        jsonInst["newSalt"]
        jsonInst["newHash"]
        return True
    except:
        print("required field for updateUser: oldUsername, newUsername, newSalt, newHash")
        return False


def createTierList(jsonInst):
    try:
        jsonInst["title"]
        jsonInst["username"]
        return True
    except:
        print("required field for createTierList: title, username")
        return False


def updateTierList(jsonInst):
    try:
        jsonInst["oldTitle"]
        jsonInst["newTitle"]
        jsonInst["username"]
        jsonInst["tiers"]
        return True
    except:
        print("required field for updateTierList: oldTitle, newTitle, username, tiers")
        return False


def deleteTierList(jsonInst):
    try:
        jsonInst["username"]
        jsonInst["title"]
        return True
    except:
        print("required field for deleteTierList: username, title")
        return False


