"""
Controller for /admin service.

Handles all administrative functions that are not 
meant for the user such as bitcoin protocol-specific 
information like blockcounts, difficulty, transaction counts, 
etc.

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

# Runs all modules with the latest changes instead of cached version, useful for dev
from gluon.custom_import import track_changes
track_changes(True)

from bitcoin_client import BitcoinClient

def getBlockcount():
    client = BitcoinClient()
    blockcount = client.getblockcount()
    return dict(message=T(str(blockcount)))