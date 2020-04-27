'''
send email handler
'''

import json
import urllib3


http = urllib3.PoolManager()

def sendTestEmail(name, mobile_number, email):
    data = {"email":email, "name":name, "phone": mobile_number}
    encoded_data = json.dumps(data).encode('utf-8')
    # URL = "https://21a94ec1.ngrok.io/sendMail"
    URL = "https://webhook-c17hawke.herokuapp.com/sendMail"
    response = http.request('POST', URL, headers={'Content-Type': 'application/json'}, body=encoded_data)
    return response.data.decode('utf-8')

def lambda_handler(event, context):
    name= event['currentIntent']['slots']['name']
    mobile_number = event['currentIntent']['slots']['phone']
    email = event['currentIntent']['slots']['email']
    result = sendTestEmail(name, mobile_number, email)
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