'''
LMBDA FUNCTION FOR AWS LEX
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''

# gets Covid data world wise

import json
import urllib3


# PoolManager is used when you want to make req to multiple hosts
# read about it here=> https://urllib3.readthedocs.io/en/1.2.1/managers.html
http = urllib3.PoolManager()

def getCovidStatus(country):
    '''gets the covid status country wise'''
    data = {"country":country}
    encoded_data = json.dumps(data).encode('utf-8')
    # URL = "https://21a94ec1.ngrok.io/covidWorld" # url for local testing
    URL = "https://webhook-c17hawke.herokuapp.com/covidWorld"
    response = http.request('POST', URL, headers={'Content-Type': 'application/json'}, body=encoded_data)
    return response.data.decode('utf-8')

def lambda_handler(event, context):
    '''
    This is the entry point for lamda function.
    It gets triggered when the even attached to it gets triggered.
    read about this here=> https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
    '''
    try:
        # extract country name
        country = event['currentIntent']['slots']['country']
        result = getCovidStatus(country)

        # extract the fullFilmenttext from the result obtained
        status = json.loads(result).get("fullFilmenttext")

        # put the status in a f string in a proper readable format
        result = f"""For country {status['country']},\n1. total active cases:{status['active']},\n2. total confirmed cases:{status['confirmed']},\n3. total deaths:{status['deaths']} and\n4. total recovered:{status['recovered']}"""

        # embed the result into the following response var and return resuponse
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
        # return response in case of any failure
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
