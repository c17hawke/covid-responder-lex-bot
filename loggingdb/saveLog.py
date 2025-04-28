'''
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''

from pymongo import MongoClient
import time
import json


class Log:
    '''
    It logs the data into cloud.mongodb.com
    '''
    def __init__(self, dbName="responder_googledb", MAX_RECORDS=100, dbPASSWORD=None, clusterName=None):
        self.MAX_RECORDS = MAX_RECORDS
        self.dbName = dbName
        self.dbPASSWORD = dbPASSWORD
        self.clusterName = clusterName
        
        # connection string is optained fromt the mongodb cloud
        self.connectionString= f"mongodb+srv://responder_google01:{self.dbPASSWORD}@{self.clusterName}.mongodb.net/test?retryWrites=true&w=majority"        
        self.client = MongoClient(self.connectionString)
        
    def insertLog(self, enterLog=None):
        '''Method to insert logs into the cloud mongodb'''
        # get the db
        db = self.client.get_database(self.dbName)
        
        # get the records in which you wish to log data
        records = db.responder_google01

        # only enter into records if it hasn't reached the max_records
        # max_records=100 by default
        if records.count_documents({}) <= self.MAX_RECORDS:
            # get current date and time
            self.date, self.time = time.strftime("%Y-%m-%d|%H:%M:%S").split("|")
            self.client = MongoClient(self.connectionString)

            # save log, date, and time into a new record var
            new_record = {"date":self.date,
                         "time":self.time,
                         "log":json.dumps(enterLog)} # had to jsonify
            # insert the new record and return the success msg       
            records.insert_one(new_record)
            return "Logged Successfully"
        else:
            return "MAX records reached. Delete previous records"