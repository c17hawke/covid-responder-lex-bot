from pymongo import MongoClient
import time
from base64 import b64encode
import json


class Log:
    def __init__(self, dbName="responder_googledb", MAX_RECORDS=100, dbPASSWORD=None):
        self.MAX_RECORDS = MAX_RECORDS
        self.dbName = dbName
        self.dbPASSWORD = dbPASSWORD
        self.connectionString= f"mongodb+srv://responder_google01:{self.dbPASSWORD}@cluster0-cjxui.mongodb.net/test?retryWrites=true&w=majority"        
        self.client = MongoClient(self.connectionString)
        
    def insertLog(self, enterLog=None):
        db = self.client.get_database(self.dbName)
        records = db.responder_google01 
        if records.count_documents({}) <= self.MAX_RECORDS:
            self.date, self.time = time.strftime("%Y-%m-%d|%H:%M:%S").split("|")
            self.client = MongoClient(self.connectionString)
            new_record = {"date":self.date,
                         "time":self.time,
                         "log":json.dumps(enterLog)} # had to jsonify
       
            records.insert_one(new_record)
            return "Logged Successfully"
        else:
            return "MAX records reached. Delete previous records"