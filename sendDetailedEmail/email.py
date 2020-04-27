'''
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''

# import neccessary libs and modules
import smtplib
import os
from email.message import EmailMessage
from getCredentials.read import ConfigReader


# define paths for attchments and HTML tempplate to send
CURRFOLDER="sendDetailedEmail"
# HTML_TEMPLATE_NAME = "DLM_Template.html"
HTML_TEMPLATE_NAME = "Template_corona_info.html"
HTML_TEMPLATE_PATH = os.path.join(CURRFOLDER, HTML_TEMPLATE_NAME)

# get the auth keys to send the mail
AUTH_DATA = ConfigReader()
eMAIL = AUTH_DATA.read_config()["eMAILsender"]
ePASSKEY = AUTH_DATA.read_config()["ePASSKEY"]

class MailAttachment:
	'''
	This class sends mail to the client by attaching necessary attachment
	It attaches an HTML template as well.
	'''
	def __init__(self, clientEmail=None):
		self.clientEmail = clientEmail

	def send(self):
		# put the Subject, From and To data for email
		msg = EmailMessage()
		msg['Subject'] = "Detailed Information about Covid-19"
		msg['From'] = eMAIL
		msg['To'] = self.clientEmail

		# add the text content which is shown if HTML is off at the client
		msg.set_content('Hi,\n\tPlease find the attachment below. \nRegards,\nSunny')
		# attach the HTML content
		with open(HTML_TEMPLATE_PATH, "r") as f:
			html_content = f.read()
		
		msg.add_alternative(html_content, subtype='html')
		
		# adding other attachements
		pdf_files = ['FAQ1.pdf']
		for file in pdf_files:
			path = os.path.join(CURRFOLDER, file)
			with open(path, "rb") as f:
				file_data = f.read()
				file_name = f.name.split("/")[-1]
			
			msg.add_attachment(file_data, maintype='application', 
			subtype='octet-stream', filename=file_name)

		# login with the auth keys and send the email
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		    smtp.login(eMAIL, ePASSKEY)
		    print("sending email...")
		    smtp.send_message(msg)
		    print("email Sent")


			