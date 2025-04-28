'''
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''
from flask import Flask, request, make_response, jsonify
import json
import os
from flask_cors import cross_origin, CORS
import requests
from covidInfo.covidData import CovidCasesIndia
from sendDetailedEmail.email import MailAttachment
from getCredentials.read import ConfigReader
from covid import Covid
from loggingdb.saveLog import Log

# get required autherization 
AUTH_DATA = ConfigReader()
dbPASSWORD = AUTH_DATA.read_config()["dbPASSWORD"]
clusterName = AUTH_DATA.read_config()["clusterName"]
app = Flask(__name__)

class ProcessingReq:
    '''
    saves logs to a remote mongoDb database hosted at 
    https://cloud.mongodb.com
    '''
    def __init__(self, password=dbPASSWORD):
        self.dbPWD = password

    def saveLogs(self, query=None, MAX_REC=1000):
        '''
        it saves queries made by the user spcially -
        1. Name, email, phone
        2. Pincode details
        3. Country wise covide status

        Max records to be saved in the db is set to 1000 by default
        This can be changed if space is not an issue.
        '''
        log = Log(MAX_RECORDS=MAX_REC, dbPASSWORD=self.dbPWD, clusterName=clusterName)
        log.insertLog(enterLog=query)
        return "Logging successfull"

def logDetails(whoAmI=None, query=None):
    '''
    it takes 2 args-
    1. whoAmI= user or bot
    2. query= inputs by user or bot
    It saves data in db using ProcessingReq Class
    '''
    process = ProcessingReq(password=dbPASSWORD)
    process.saveLogs({"user":whoAmI, "query":query})


# route to save sendmail
@app.route("/sendMail", methods=["POST"])
@cross_origin()
def sendMail():
    try:
        # get client info
        clientInfo = request.get_json()
        # log the details in the db
        logDetails(whoAmI="user", query=clientInfo['name'])

        # get user's email to send the FAQ
        clientEmail = clientInfo['email']
        clientName = clientInfo['name']
        clientPhone = clientInfo['phone']

        # send mail to the user 
        # d is a temp var can be used for debuging 
        d = MailAttachment(clientEmail=clientEmail).send()
        # save the response in dictionary
        response = {"fullFilmenttext":f"mail sent to {clientEmail}"}
        # save the response in the db and return response
        logDetails(whoAmI="bot", query=response)
        return response
    except Exception as e:
        # in case of failure save error log and send the response with error msg
        response = {"fullFilmenttext":f"process failed due to Error:{e}"}
        logDetails(whoAmI="bot", query=response)
        return response


# route to get covid data PIN code wise
@app.route("/covidInfo", methods=['POST'])
@cross_origin()
def covidInfo():
    try:
        # get user's request details
        dataRequest = request.get_json()
        # log the details in the db
        logDetails(whoAmI="user", query=dataRequest)
        
        # send details to the user as per PIN and State

        # if keys contains PIN
        if "PIN" in dataRequest.keys():
            # get details wrt PIN
            obj = CovidCasesIndia(PIN=dataRequest["PIN"])
            result = obj.get_data()
        if "state" in dataRequest.keys():
            # get detila wrt state
            obj = CovidCasesIndia(state=dataRequest["state"])
            result = obj.get_data()
        # record response in dict format and return
        response = {"fullFilmenttext":result}
        logDetails(whoAmI="bot", query=response)
        return response
    except Exception as e:
        # in case of failure save error log and send the response with error msg
        response = {"fullFilmenttext":f"process failed due to Error:{e}"}
        logDetails(whoAmI="bot", query=response)
        return response

# route to get covid data wrt World. It follows same flow as PIN
@app.route("/covidWorld", methods=['POST'])
@cross_origin()
def covidWorld():
    try:
        dataRequest = request.get_json()
        logDetails(whoAmI="user", query=dataRequest)
        country = dataRequest["country"]
        covid = Covid()
        result = covid.get_status_by_country_name(country)
        response = {"fullFilmenttext":result}
        logDetails(whoAmI="bot", query=response)
        return response
    except Exception as e:
        response = {"fullFilmenttext":f"process failed due to Error:{e}"}
        logDetails(whoAmI="bot", query=response)
        return response


if __name__=="__main__":
    try:
        # get PORT from env var
        port = int(os.getenv('PORT', 5000))
        print("Starting app on port %d" % port)
        # run app in dev mode
        app.run(debug=False, port=port, host='0.0.0.0')
    except Exception as e:
        raise e