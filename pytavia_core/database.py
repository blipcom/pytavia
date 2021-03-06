import time
import copy
import pymongo
import os
import sys
import model
import config
import random

from bson.objectid import ObjectId

db_conn_completed = False

db_conn = {}
for row in config.G_DATABASE_CONNECT:
    db_conn[row["dbname"]] = row["dbstring"]
#end for

db_active_con = {}
for row in config.G_DATABASE_CONNECT:
    db_active_con[row["dbname"]] = None
#end for

db = model.db

def connect_db():
    for row in config.G_DATABASE_CONNECT:
        if db_active_con[row["dbname"]] == None:
            db_active_con[row["dbname"]] = pymongo.MongoClient( db_conn[row["dbname"]] )
        # end if
    #end for
    db_conn_completed = True
#end def

def get_database(database_name):
    return db_active_con[database_name]
# end def

def get_db_conn(db_conn):
    # make sure we are connected to the database
    if not db_conn_completed:
        connect_db()
    #end if

    # get the specific handle we want to connect to
    handle = db_active_con[db_conn][db_conn]
    handle.db_conn.find({})
    return handle
#end def

def get_record(db_table):
    timestamp = int(time.time()) * 1000
    record    = db[db_table]
    record["rec_timestamp"    ] = timestamp
    record["rec_timestamp_str"] = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))
    )
    record["_id" ] = ObjectId()
    record["pkey"] = str( record["_id"] )
    return copy.deepcopy( record )
#end def

def new(db_handle, db_table):
    timestamp = int(time.time()) * 1000
    record    = db[db_table]
    record["__db__name__"     ] = db_table
    record["rec_timestamp"    ] = timestamp
    record["rec_timestamp_str"] = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))
    )

    now_time        = int(time.time() * 1000)
    random_int      = random.randint( config.G_RANDOM_START , config.G_RANDOM_END )

    _id = ObjectId()
    record["ipkey"] = str( _id )
    record["pkey" ] = str( _id ) + "-" + str(now_time) + "-" + str(random_int)

    mongo_record_model      = model.mongo_model( record , record , db_handle )
    return  mongo_record_model 
#end def

def load(db_handle, db_table):
    record                  = db[db_table]
    record["__db__name__" ] = db_table
    mongo_record_model      = model.mongo_model( {} , record , db_handle )
    return mongo_record_model
#end def
#
