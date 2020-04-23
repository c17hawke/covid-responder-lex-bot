"""
Author: Sunny Bhaveen Chandra
Version: 2.0
Dated: Apr 19, 2020
"""
import pandas as pd
import requests
import json
import os

# MAIN_DF = "/content/drive/My Drive/iCompetition/pincodeMain_Odisha_update.csv"
UTILS = "covidInfo"
PINCODE_DATA_PATH = os.path.join(UTILS, "pinCodeData.csv")

class CovidCasesIndia:
    def __init__(self, PIN=None, state=None, df_path = PINCODE_DATA_PATH):
        self.PIN = PIN
        self.state = state
        self.df = pd.read_csv(df_path)
        self._stateAPI = "https://api.rootnet.in/covid19-in/stats/latest"
        self._districtAPI = "https://api.covid19india.org/state_district_wise.json"

    def get_data(self):
        if self.PIN is not None:
            return {"district":self._get_data_fromPIN(), "state":self._get_data_fromSTATE()}
        else:
            return {"state":self._get_data_fromSTATE()}

    def _get_district_data(self, state, district):
        json_data = requests.get(self._districtAPI).json()
        d_data = json_data[state]["districtData"][district]
        return d_data

    def _get_data_fromPIN(self):
        def query_pincode(PIN):
            try:
                if (type(PIN) in [int, str]) and (self.df["Pincode"].isin([PIN]).any()): # already_read
                    mask = int(PIN) == self.df['Pincode']
                    result = self.df[mask]
                    return result
                return "Invalid PIN code or data is not availble"
            except Exception as e:
                return str(e)
        query = query_pincode(self.PIN)
        self.state = query.State.iloc[0]
        self.dist = query.District.iloc[0]
        # print(self.state, self.dist)
        try:
            return {"district":self.dist, "confirmed":self._get_district_data(self.state, self.dist)['confirmed']}
        except:
            return {"district":self.dist, "confirmed":0}

    def _get_data_fromSTATE(self):
        json_data = requests.get(self._stateAPI).json()
        def query_state_wise(query):
            for loc in json_data["data"]["regional"]:
                if loc['loc'] == query:
                    return loc
                    break
        return query_state_wise(self.state)