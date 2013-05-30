from bitcoinrpc.authproxy import AuthServiceProxy

def getBlockcount():
	bitcoind = AuthServiceProxy("https://bitcoinrpc:asdfasdf@127.0.0.1:8332")
	blockcount = bitcoind.getblockcount()
	return dict(message=T(str(blockcount)))
	#return blockcount
	#
