'''
LMBDA FUNCTION FOR AWS LEX
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''

# sends mail to the user with FAQ attached

import json
import urllib3


http = urllib3.PoolManager()

def sendTestEmail(name, mobile_number, email):
    data = {"email":email, "name":name, "phone": mobile_number}
    encoded_data = json.dumps(data).encode('utf-8')
    # URL = "https://21a94ec1.ngrok.io/sendMail" # url for local testing
    URL = "https://webhook-c17hawke.herokuapp.com/sendMail"
    response = http.request('POST', URL, headers={'Content-Type': 'application/json'}, body=encoded_data)
    return response.data.decode('utf-8')

def lambda_handler(event, context):
    '''
    This is the entry point for lamda function.
    It gets triggered when the even attached to it gets triggered.
    read about this here=> https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
    '''
    # extract name, mobile_number and email
    name= event['currentIntent']['slots']['name']
    mobile_number = event['currentIntent']['slots']['phone']
    email = event['currentIntent']['slots']['email']
    result = sendTestEmail(name, mobile_number, email)

    # extract the fullFilmenttext and embed the result into response var
    # and then return the response
    result = json.loads(result).get("fullFilmenttext")
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message":{
                "contentType": "SSML",
                "content": f"{result}. Please let us know if we can assist you with any other information."
            },
        }
    }
    return response