from bitcoinclient import BitcoinClient

def getBlockcount():
    client = BitcoinClient()
    blockcount = client.get_blockcount()
    return dict(message=T(str(blockcount)))