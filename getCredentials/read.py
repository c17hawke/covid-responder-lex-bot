'''
# Author: Sunny Bhaveen Chandra
# Contact: sunny.c17hawke@gmail.com
# dated: April, 23, 2020
'''
import configparser
import os

# get the path of config file 
CURRENT_FOLDER = "getCredentials"
CONFIG_FILE = "config.ini"
CONFIG_FILE_PATH = os.path.join(CURRENT_FOLDER, CONFIG_FILE)

class ConfigReader:
    '''
    It read the following from the config file-
    1. senders email
    3. login keys of sender's email
    3. passwords for the database
    '''
    def __init__(self):
        self.configFileName = CONFIG_FILE_PATH
        
    def read_config(self):
        '''reads the congfig file to get details'''
        self.config = configparser.ConfigParser()
        self.config.read(self.configFileName)
        self.configuration = self.config["DEFAULT"]
        # extract the secret info from the config file and return the info
        self.eMAILsender = self.configuration["eMAILsender"]
        self.ePASSKEY = self.configuration["ePASSKEY"]
        self.dbPASSWORD = self.configuration['dbPASSWORD']
        return self.configuration