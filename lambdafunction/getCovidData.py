'''
LMBDA FUNCTION FOR AWS LEX
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''

# gets covid data pin wise

import json
import urllib3

# PoolManager is used when you want to make req to multiple hosts
# read about it here=> https://urllib3.readthedocs.io/en/1.2.1/managers.html
http = urllib3.PoolManager()

def getCovidStatus(PIN):
    '''gets the covid status from the webhook'''
    data = {"PIN":PIN}
    # encode data 
    encoded_data = json.dumps(data).encode('utf-8')
    # URL = "https://21a94ec1.ngrok.io/covidInfo" # use only for local test

    # Webhook URL hosted on Heroku
    URL = "https://webhook-c17hawke.herokuapp.com/covidInfo"

    # Make a post request to the URL with header and body containing encoded data
    response = http.request('POST', 
    URL, 
    headers={'Content-Type': 'application/json'}, 
    body=encoded_data)

    # decode response and return the data
    return response.data.decode('utf-8')

def lambda_handler(event, context):
    '''
    This is the entry point for lamda function.
    It gets triggered when the even attached to it gets triggered.
    read about this here=> https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
    '''
    try:
        # extract PIN from the event 
        PIN = event['currentIntent']['slots']['PIN']
        
        # get Covid info from the following functions -
        result = getCovidStatus(PIN)
        
        # extract fullFilment text from the result
        result = json.loads(result).get("fullFilmenttext")

        # extract dist and state wise data
        districtData = result.get("district")
        stateData = result.get("state")

        # store the dict result as a meaningfule string in dist and state vars
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

        # save the response and return
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
        # return response in case of any failure
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
        

