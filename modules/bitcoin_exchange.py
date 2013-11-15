"""
Bitcoin Exchange

Provides a wrapper class for all the bitcoin exchanges and exchange libraries. Handles logic for 
automatic switching of exchanges at runtime.

CampBX 1.0.5 Python library: https://pypi.python.org/pypi/campbx/1.0.5
BitStamp API: https://www.bitstamp.net/api/

Author: Henry Nguyen
"""

import json
import urllib2
# from campbx import CampBX

class BitcoinExchange:
    # TODO: Figure out how to implement this class as a Singleton
    
    def __init__(self):
        return None
    
    def getlastprice(self):
        response = urllib2.urlopen("https://www.bitstamp.net/api/ticker/")
        data = json.load(response)
        return data["last"]