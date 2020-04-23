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

AUTH_DATA = ConfigReader()
dbPASSWORD = AUTH_DATA.read_config()["dbPASSWORD"]

app = Flask(__name__)

class ProcessingReq:
    def __init__(self, password=dbPASSWORD):
        self.dbPWD = password

    def saveLogs(self, query=None, MAX_REC=1000):
        log = Log(MAX_RECORDS=MAX_REC, dbPASSWORD=self.dbPWD)
        log.insertLog(enterLog=query)
        return "Logging successfull"

def logDetails(whoAmI=None, query=None):
        process = ProcessingReq(password=dbPASSWORD)
        process.saveLogs({"user":whoAmI, "query":query})

@app.route("/sendMail", methods=["POST"])
@cross_origin()
def sendMail():
    try:
        # print(request.get_json())
        clientInfo = request.get_json()
        logDetails(whoAmI="user", query=clientInfo['name']) # only saving name
        clientEmail = clientInfo['email']
        clientName = clientInfo['name']
        clientPhone = clientInfo['phone']
        d = MailAttachment(clientEmail=clientEmail).send()
        response = {"fullFilmenttext":f"mail sent to {clientEmail}"}
        logDetails(whoAmI="bot", query=response)
        return response
    except Exception as e:
        response = {"fullFilmenttext":f"process failed due to Error:{e}"}
        logDetails(whoAmI="bot", query=response)
        return response


@app.route("/covidInfo", methods=['POST'])
@cross_origin()
def covidInfo():
    try:
        # print(request.get_json())
        dataRequest = request.get_json()
        logDetails(whoAmI="user", query=dataRequest)
        if "PIN" in dataRequest.keys():
            obj = CovidCasesIndia(PIN=dataRequest["PIN"])
            result = obj.get_data()
        if "state" in dataRequest.keys():
            obj = CovidCasesIndia(state=dataRequest["state"])
            result = obj.get_data()
        # print(result)
        response = {"fullFilmenttext":result}
        logDetails(whoAmI="bot", query=response)
        return response
    except Exception as e:
        response = {"fullFilmenttext":f"process failed due to Error:{e}"}
        logDetails(whoAmI="bot", query=response)
        return response


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
        port = int(os.getenv('PORT', 5000))
        print("Starting app on port %d" % port)
        app.run(debug=False, port=port, host='0.0.0.0')
    except Exception as e:
        raise e