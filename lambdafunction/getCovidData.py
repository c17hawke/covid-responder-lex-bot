'''
gets covid data pin wise
'''

import json
import urllib3

http = urllib3.PoolManager()

def getCovidStatus(PIN):
    data = {"PIN":PIN}
    encoded_data = json.dumps(data).encode('utf-8')
    # URL = "https://21a94ec1.ngrok.io/covidInfo"
    URL = "https://webhook-c17hawke.herokuapp.com/covidInfo"
    response = http.request('POST', URL, headers={'Content-Type': 'application/json'}, body=encoded_data)
    return response.data.decode('utf-8')

def lambda_handler(event, context):
    try:
        PIN = event['currentIntent']['slots']['PIN']
        result = getCovidStatus(PIN)
        result = json.loads(result).get("fullFilmenttext")
        districtData = result.get("district")
        stateData = result.get("state")
        distWise = "{} (PIN: {}),\n\
# total confirmed Cases are {}".format(districtData['district'],PIN, 
            districtData['confirmed'])
        stateWise = "{},\n\
1. confirmed Cases (Foreign): {},\n\
2. confirmed Cases (Indian): {},\n\
3. deaths: {},\n\
4. discharged: {},\n\
5. total Confirmed: {}".format(stateData["loc"],
        stateData["confirmedCasesForeign"],
        stateData["confirmedCasesIndian"],
        stateData["deaths"],
        stateData["discharged"],
        stateData["totalConfirmed"])
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message":{
                    "contentType": "SSML",
                    "content": f"for your district >> \n{distWise} \nand\nfor your state or UT >> \n{stateWise}.\n\nIf you have any other query then please ask :)"

                },
            }
        }
        return response
    
    except:
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message":{
                    "contentType": "SSML",
                    "content": f"I'm sorry but I think PIN code was invalid. Kindly check and please try again :)"
                },
            }
        }
        

