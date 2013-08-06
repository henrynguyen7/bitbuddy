# Runs all modules with the latest changes instead of cached version, useful for dev
from gluon.custom_import import track_changes
track_changes(True)

from bitcoinclient import BitcoinClient

def getBlockcount():
    client = BitcoinClient()
    blockcount = client.getblockcount()
    return dict(message=T(str(blockcount)))