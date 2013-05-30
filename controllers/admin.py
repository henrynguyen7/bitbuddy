import sys
sys.path.append('../private')
from bitcoind import bitcoindIP, bitcoindPort, bitcoindUser, bitcoindPass, bitcoindProtocol
from bitcoinrpc.authproxy import AuthServiceProxy

def getBlockcount():
	bitcoind = AuthServiceProxy(bitcoindProtocol + bitcoindUser + ":" + bitcoindPass + "@" + bitcoindIP + ":" + bitcoindPort) 
	blockcount = bitcoind.getblockcount() 
	return dict(message=T(str(blockcount)))
	#return blockcount
	#print(blockcount)

#getBlockcount()
