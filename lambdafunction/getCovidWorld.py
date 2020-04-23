'''
gets Covid data world wise
'''

import json
import urllib3

http = urllib3.PoolManager()

def getCovidStatus(country):
    data = {"country":country}
    encoded_data = json.dumps(data).encode('utf-8')
    # URL = "https://21a94ec1.ngrok.io/covidWorld"
    URL = "https://webhook-c17hawke.herokuapp.com/covidWorld"
    response = http.request('POST', URL, headers={'Content-Type': 'application/json'}, body=encoded_data)
    return response.data.decode('utf-8')

def lambda_handler(event, context):
    try:
        country = event['currentIntent']['slots']['country']
        result = getCovidStatus(country)
        status = json.loads(result).get("fullFilmenttext")
        result = f"""For country {status['country']},\n1. total active cases:{status['active']},\n2. total confirmed cases:{status['confirmed']},\n3. total deaths:{status['deaths']} and\n4. total recovered:{status['recovered']}"""
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message":{
                    "contentType": "SSML",
                    "content": f"{result}.\n\n If you have any other query then please ask :)"
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
                    "content": f"I'm sorry but I feel that the country name was incorrect. Please check the country name and try again :)"
                },
            }
        }
