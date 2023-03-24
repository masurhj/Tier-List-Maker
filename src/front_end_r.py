import connections
import time
    
def userExists(username):
    mUser = None
    oUserLi = None
    connections.tryConnections()
    print("checking user exists with front end")
    if (connections.oConnected):
        try:
            oUserLi = connections.oClient.command("SELECT FROM USER WHERE username='%s'" % (username))
        except:
            connections.mConnected = False
    if (connections.mConnected):
        try:
            mUser = connections.userDB.find_one({"username": username})
        except:
            connections.oConnected = False
    #only needs to exist on one DB to be considered existing
    if (not (connections.mConnected or connections.oConnected)):
        #returns None if dbs are no longer connected
        print("NO CONNECTION FOR USR EXISTS")
        return None
    else:
        return (mUser is not None) or ((oUserLi is not None) and (len(oUserLi) > 0))

def tierListExists(username, title):
    mList = None
    oList = None
    connections.tryConnections()
    print("checking tier list exists with front end")
    if(connections.oConnected):
        try:
            oList = connections.oClient.command("SELECT FROM (TRAVERSE * FROM (SELECT FROM USER WHERE username = '%s')) WHERE title='%s' AND  @class = 'TIERLIST'"
            % (username, title))
        except:
            connections.oConnected = False
    if(connections.mConnected):
        try:
            mList = connections.tierlistDB.find_one({"username": username, "title": title})
        except:
            connections.mConnected = False
    if (not (connections.mConnected or connections.oConnected)):
        #returns None if dbs are no longer connected
        print("NO CONNECTION FOR TIERLIST EXISTS")
        return None
    else:
        return (mList is not None) or ((oList is not None) and (len(oList) > 0))
    
def getTierLists(username):
    mTierLists = None
    oTierLists = None
    connections.tryConnections()
    if(connections.oConnected):
        try:
            oTierLists = connections.oClient.command("SELECT FROM (TRAVERSE * FROM (SELECT FROM USER WHERE username = '%s')) WHERE @class = 'TIERLIST'" % (username))
            tids = oTierLists
            oTierLists = []
            for curId in tids:
                if (curId is None):
                    continue
                oTierLists.append(curId.title) 
        except:
            connections.oConnected = False

    if(connections.mConnected and not connections.oConnected):
        try:
            mUser = connections.userDB.find_one({"username": username})
            if (mUser is None):
                print("user not found")
                return
            if ('tierlist-ids' not in mUser):
                print("user has not yet made any tierlists")
                return []
            tids = mUser['tierlist-ids']
            mTierLists = []
            for curId in tids:
                t = connections.tierlistDB.find_one({"_id": curId})
                if (t is None):
                    continue
                mTierLists.append(t["title"])
        except:
            connections.mConnected = False
    if (not (connections.mConnected or connections.oConnected)):
        #returns None if dbs are no longer connected
        print("NO CONNECTION FOR TIERLIST EXISTS")
        return None
    else:
        if(oTierLists):
            return oTierLists
        elif(mTierLists):
            return mTierLists
        else:
            return []

def getTierListByTitle(username,title):
    mTierList = None
    oTierList = None
    connections.tryConnections()
    if(connections.oConnected):
        try:
            oTierList = connections.oClient.command("SELECT FROM (TRAVERSE * FROM (SELECT FROM USER WHERE username = '%s')) WHERE title='%s' AND  @class = 'TIERLIST'"
            % (username, title))
            doc = {
                "title" : oTierList[0].title,
                "tiers" : oTierList[0].tiers
            }
            print(doc)
            oTierList = doc
        except:
            connections.oConnected = False
    if(connections.mConnected and not connections.oConnected):
        try:
            mUserList = connections.userDB.find({"username": username})
            tids = mUserList[0]['tierlist-ids']
            tl = connections.tierlistDB.find({"_id": tids[0]})
            print(tl[0])
            mTierList = tl[0]
        except:
            connections.mConnected = False
    if (not (connections.mConnected or connections.oConnected)):
        #returns None if dbs are no longer connected
        print("NO CONNECTION FOR TIERLIST EXISTS")
        return None
    else:
        if(oTierList):
            return oTierList
        elif(mTierList):
            return mTierList
        else:
            return []


    #only needs to exist on one DB to be considered existing
    # tids = connections.userDB.find_one({"username": username})["tierlist-ids"]
    # mTierList = connections.tierlistDB.find_one({"title": title, "_id": {"$in": tids}})
    # oUser = connections.oClient.command("SELECT(SELECT FROM USER WHERE username='%s')" % (username))
    # oTierListLi = connections.oClient.command("SELECT FROM TIERLIST WHERE title='%s' AND in.out[@Class = 'USER'].username = '%s'"
    #         % (title, username))
    # return (mTierList is not None) or len(oTierListLi) > 0