from bitcoinrpc.authproxy import AuthServiceProxy

bitcoind = AuthServiceProxy("http://bitcoinrpc:asdfasdf@127.0.0.1:8332")

info = bitcoind.getinfo()
blockcount = bitcoind.getblockcount()
difficulty = bitcoind.getdifficulty()
isGenerating = bitcoind.getgenerate()

print "info: ", info
print "blockcount: ", blockcount
print "difficulty: ", difficulty
print "isGenerating: ", isGenerating