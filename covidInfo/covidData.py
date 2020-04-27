"""
Author: Sunny Bhaveen Chandra
Version: 2.0
Dated: Apr 19, 2020
"""
import pandas as pd
import requests
import json
import os

# get path of PINCODE csv file
UTILS = "covidInfo"
PINCODE_DATA_PATH = os.path.join(UTILS, "pinCodeData.csv")

class CovidCasesIndia:
    '''
    This serves you with State and PINCODE wise data.
    '''
    def __init__(self, PIN=None, state=None, df_path = PINCODE_DATA_PATH):
        self.PIN = PIN
        self.state = state
        # read csv
        self.df = pd.read_csv(df_path)
        # APIs to get state and district wise covid data
        self._stateAPI = "https://api.rootnet.in/covid19-in/stats/latest"
        self._districtAPI = "https://api.covid19india.org/state_district_wise.json"

    def get_data(self):
        '''gets data wrt to PIN or state'''
        if self.PIN is not None:
            return {"district":self._get_data_fromPIN(), "state":self._get_data_fromSTATE()}
        else:
            return {"state":self._get_data_fromSTATE()}

    def _get_district_data(self, state, district):
        '''gets districts wise data'''
        # read json paypload from district API
        json_data = requests.get(self._districtAPI).json()
        # extract district data and return the result
        d_data = json_data[state]["districtData"][district]
        return d_data

    def _get_data_fromPIN(self):
        '''get PIN wise data'''
        def query_pincode(PIN):
            '''gets state and district name from csv by using PINCODE provided'''
            try:
                # check if PIN is valid
                if (type(PIN) in [int, str]) and (self.df["Pincode"].isin([PIN]).any()): # already_read
                    mask = int(PIN) == self.df['Pincode']
                    result = self.df[mask]
                    return result
                return "Invalid PIN code or data is not availble"
            except Exception as e:
                return str(e)
        query = query_pincode(self.PIN)
        # extract state and distt. name from query
        self.state = query.State.iloc[0]
        self.dist = query.District.iloc[0]
        try:
            # return this if data of distt is present
            return {"district":self.dist, "confirmed":self._get_district_data(self.state, self.dist)['confirmed']}
        except:
            # return this if data is not found from the requested API
            return {"district":self.dist, "confirmed":0}

    def _get_data_fromSTATE(self):
        '''gets data state wise from the API'''
        json_data = requests.get(self._stateAPI).json()
        def query_state_wise(query):
            for loc in json_data["data"]["regional"]:
                if loc['loc'] == query:
                    return loc
                    break
        return query_state_wise(self.state)