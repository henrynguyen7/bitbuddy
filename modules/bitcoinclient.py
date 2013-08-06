"""
Bitcoin Client

Provides a wrapper class for the bitcoind client. Initially
will use bitcoind as the client but should later be upgraded
to a more secure client such as Armory.

Coding style guide: http://www.python.org/dev/peps/pep-0008/
"""

# Runs all modules with the latest changes instead of cached version, useful for dev
from gluon.custom_import import track_changes
track_changes(True)

# TODO: Move bitcoind_resources.py into ../private and figure out how to import it into here
# import sys
# sys.path.append('../private/')
from bitcoind_resources import bitcoindIP, bitcoindPort, bitcoindUser, bitcoindPass, bitcoindProtocol
from bitcoinrpc import AuthServiceProxy

class BitcoinClient:
    # TODO: Figure out how to implement this class as a Singleton

    def __init__(self):
        self.bitcoind = AuthServiceProxy(bitcoindProtocol + bitcoindUser + ":" + bitcoindPass + "@" + bitcoindIP + ":" + bitcoindPort)  

    def get_blockcount(self):
        return self.bitcoind.getblockcount()