import json
import redis
import instructions
import constants
import time


r = redis.Redis(host=constants.REDIS_VM, port=constants.REDIS_PORT)
r.ping()


while(True):
    time.sleep(constants.CLOCK)
    #obtain and parse mongo queue value
    mongoSuccess = False
    mpeekJSONStringEncoded = r.lindex(constants.MONGO_KEY, 0)
    if (mpeekJSONStringEncoded is not None):
        mpeekJSONStringDecoded = mpeekJSONStringEncoded.decode("utf-8")
        mpeekJSON = json.loads(mpeekJSONStringDecoded)
        mongoSuccess = instructions.runInstruction(mpeekJSON, constants.MONGO_KEY)

    #obtain and parse orient queue value
    orientSuccess = False
    opeekJSONStringEncoded = r.lindex(constants.ORIENT_KEY, 0)
    if (opeekJSONStringEncoded is not None):
        opeekJSONStringDecoded = opeekJSONStringEncoded.decode("utf-8")
        opeekJSON = json.loads(opeekJSONStringDecoded)
        orientSuccess = instructions.runInstruction(opeekJSON, constants.ORIENT_KEY)

    #attempt to run the mongo instruction
    #attempt to run redis instruction

    #pop queues where the instruction ran successfully (db is not down)
    if (orientSuccess):
        r.lpop(constants.ORIENT_KEY)
    if (mongoSuccess):
        r.lpop(constants.MONGO_KEY)







