from bitcoinrpc.authproxy import AuthServiceProxy
from bitcoindLogin import *

def getBlockcount():
	bitcoind = AuthServiceProxy("http://" + bitcoindUser + ":" + bitcoindPwd + "@127.0.0.1:8332")
	blockcount = bitcoind.getblockcount()
	return dict(message=T(str(blockCount)))
	#return blockcount
	#print(blockcount)

#getBlockcount()
