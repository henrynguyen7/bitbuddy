"""
Bitcoin Client

Provides a wrapper class for the bitcoind client, to allow for easy modularity
so that a different bitcoin daemon can be used at a later time, as needed. 

Initially will use bitcoind as the client but will later be upgraded
to Armory which is much more secure due to separate, offline storage of 
private keys and other sensitive data.

Author: Henry Nguyen
"""

import json
import os
from bitcoinrpc import AuthServiceProxy

# load bitcoind client login credentials from resource file
dir = os.path.dirname(__file__)
resourceFile = os.path.join(dir, "../private", "resources.json")
resource_file = os.path.join(request.folder, "private", "resources.json")
with open(resource_file) as resource:
    resource_data = json.load(resource)

# TODO: Put these into a dict or some other Python data struct for this kinda thing
bitcoind_username, bitcoind_password, bitcoind_protocol, bitcoind_ip, bitcoind_port = resource_data["bitcoind"]["username"], resource_data["bitcoind"]["password"], resource_data["bitcoind"]["protocol"], resource_data["bitcoind"]["ip"], resource_data["bitcoind"]["port"]

class BitcoinClient(object):
    # TODO: Figure out how to implement this class as a Singleton
    # TODO: Add/fix parameters where needed per https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_Calls_list
    
    def __init__(self):
        """Initializes the class with the bitcoind client."""
        self.bitcoind = AuthServiceProxy(bitcoind_protocol + "://" + bitcoind_username + ":" + bitcoind_password + "@" + bitcoind_ip + ":" + bitcoind_port)  
        
    # def addmultisigaddress(self, nrequired, ["key","key"], account=None):
    #     """Add a nrequired-to-sign multisignature address to the wallet.
        
    #     Each key is a bitcoin address or hex-encoded public key. 
    #     If [account] is specified, assign address to [account].
        
    #     nrequired: number of signatures to require
    #     ["key","key"]: 
    #     account: account to add to
    #     """
    #     return self.bitcoind.addmultisigaddress(nrequired, ["key","key"], account)
    
    def addnode(self, node, action):
        """Attempts add or remove <node> from the addnode list or try a connection to <node> once.
        
        node: connection node 
        action: action to take on node (possible: add/remove/onetry)
        """
        return self.bitcoind.addnode(node, action)
    
    def backupwallet(self, destination):
        """Safely copies wallet.dat to destination, which can be a directory or a path with filename.
        
        destination: directory or a path with filename to backup wallet to
        """
        return self.bitcoind.backupwallet(destination)
    
    def createmultisig(self):
        return None
    
    def createrawtransaction(self):
        return None
    
    def decoderawtransaction(self):
        return None
    
    def dumpprivkey(self, bitcoinaddress):
        """Reveals the private key corresponding to <bitcoinaddress>
        
        bitcoinaddress: address to reveal private key for
        """
        return self.bitcoind.dumpprivkey(bitcoinaddress)
    
    def encryptwallet(self, passphrase):
        """Encrypts the wallet with <passphrase>.
        
        passphrase: passphrase to encrypt wallet with     
        """
        return self.bitcoind.encryptwallet(passphrase)
    
    def getaccount(self, bitcoinaddress):
        """Returns the account associated with the given address.
        
        bitcoinaddress: address associated with account
        """
        return self.bitcoind.getaccount(bitcoinaddress)
    
    def getaccountaddress(self, account):
        """Returns the current bitcoin address for receiving payments to this account.
        
        account: account to return receiving address for
        """
        return self.bitcoind.getaccountaddress(account)
    
    def getaddednodeinfo(self):
        return None
    
    def getaddressesbyaccount(self, account):
        """Returns the list of addresses for the given account.
        
        account: account to return addresses for        
        """
        return self.bitcoind.getaddressesbyaccount(account)
    
    def getbalance(self, account=None, minconf=1):
        """Returns balance for server's total available balance.
        
        account: if [account] is not specified, returns the server's total available balance, otherwise returns the balance in the account.
        minconf: number of min confirmations to count
        """
        return self.bitcoind.getbalance(account, minconf)
    
    def getblock(self, hash):
        """Returns information about the block with the given hash.
        
        hash: hash to return block info for
        """
        return self.bitcoind.getblock(hash)

    def getblockcount(self):
        """Returns the number of blocks in the longest block chain."""
        return self.bitcoind.getblockcount()
        
    def getblockhash(self, index):
        """Returns hash of block in best-block-chain at <index>; index 0 is the genesis block.
        
        index: index of block to hash
        """
        return self.bitcoind.getblockhash(index)
    
    def getblocktemplate(self, params=None):
        """Returns data needed to construct a block to work on.
        
        params: 
        """
        return None
    
    def getconnectioncount(self):
        """Returns the number of connections to other nodes."""
        return self.bitcoind.getconnectioncount()
    
    def getdifficulty(self):
        """Returns the proof-of-work difficulty as a multiple of the minimum difficulty."""
        return self.bitcoind.getdifficulty()
    
    def getgenerate(self):
        """Returns true or false whether bitcoind is currently generating hashes."""
        return self.bitcoind.getgenerate()
    
    def gethashespersec(self):
        """Returns a recent hashes per second performance measurement while generating."""
        return self.bitcoind.gethashespersec()
    
    def getinfo(self):
        """Returns an object containing various state info."""
        return self.bitcoind.getinfo()
    
    def getmemorypool(self):
        return None
    
    def getmininginfo(self):
        """ Returns an object containing mining-related information:
        - blocks
        - currentblocksize
        - currentblocktx
        - difficulty
        - errors
        - generate
        - genproclimit
        - hashespersec
        - pooledtx
        - testnet
        """
        return self.bitcoind.getmininginfo()
    
    def getnewaddress(self, account=None):
        """Returns a new bitcoin address for receiving payments. 
        
        account: if [account] is specified (recommended), it is added to the address book 
        so payments received with the address will be credited to [account].
        """
        return self.bitcoind.getnewaddress(account)
    
    def getpeerinfo(self):
        """Returns data about each connected node."""
        return self.bitcoind.getpeerinfo()
    
    def getrawmempool(self):
        """Returns all transaction ids in memory pool."""
        return self.bitcoind.getrawmempool()
    
    def getrawtransaction(self):
        return None
    
    def getreceivedbyaccount(self, account=None, minconf=1):
        """Returns the total amount received by addresses with [account] in transactions with at least [minconf] confirmations. 
        
        account: if [account] not provided return will include all transactions to all accounts
        minconf: minimum number of confirmations to count        
        """
        return None
    
    def getreceivedbyaddress(self, bitcoinaddress, minconf=1):
        """Returns the total amount received by <bitcoinaddress> in transactions with at least [minconf] confirmations. 
        
        While some might consider this obvious, value reported by this only considers *receiving* transactions. 
        It does not check payments that have been made *from* this address. In other words, this is not "getaddressbalance". Works only for addresses in the local wallet, external addresses will always show 0.
        
        bitcoinaddress: address 
        minconf = minimum number of confirmations to count
        """
        return self.bitcoind.getreceivedbyaddress(bitcoinaddress, minconf)
    
    def gettransaction(self, txid):
        """Returns an object about the given transaction containing:
        - amount: total amount of the transaction
        - confirmations: number of confirmations of the transaction
        - txid: the transaction ID
        - time: time associated with the transaction[1].
        - details - An array of objects containing:
            - account
            - address
            - category
            - amount
            - fee
            
        txid: transaction id
        """
        return self.bitcoind.gettransaction(txid)
    
    def gettxout(self):
        return None
    
    def gettxoutsetinfo(self):
        """Returns statistics about the unspent transaction output (UTXO) set."""
        return self.bitcoind.gettxoutsetinfo()
    
    def getwork(self):
        return None
    
    def help(self, command=None):
        """List commands, or get help for a command.
        
        command: command to get help for
        """
        return self.bitcoind.help(command)
    
    def importprivkey(self, bitcoinprivkey, label, rescan=None):
        """Adds a private key (as returned by dumpprivkey) to your wallet. 
        
        This may take a while, as a rescan is done, looking for existing transactions.
        
        bitcoinprivkey: 
        label: 
        rescan: True/False
        """
        return self.bitcoind.importprivkey(bitcoinprivkey, label, rescan)
    
    def keypoolrefill(self):
        """Fills the keypool, requires wallet passphrase to be set."""
        return self.bitcoind.keypoolrefill()
    
    def listaccounts(self, minconf=1):
        """Returns Object that has account names as keys, account balances as values.
        
        minconf: minimum number of confirmations to count
        """        
        return self.bitcoind.listaccounts(minconf)
    
    def listaddressgroupings(self):
        """Returns all addresses in the wallet and info used for coincontrol."""
        return self.bitcoind.listaddressgroupings()
    
    def listreceivedbyaccount(self, minconf=1, includeempty=False):
        """Returns an array of objects containing:
        - account: the account of the receiving addresses
        - amount: total amount received by addresses with this account
        - confirmations: number of confirmations of the most recent transaction included
        
        minconf: minimum number of confirmations to count
        includeempty: True/False
        """
        return self.bitcoind.listreceivedbyaccount(minconf, includeempty)
    
    def listreceivedbyaddress(self, minconf=1, includeempty=False):
        """Returns an array of objects containing:
        - address: receiving address
        - account: the account of the receiving address
        - amount: total amount received by the address
        - confirmations: number of confirmations of the most recent transaction included
        
        To get a list of accounts on the system, execute bitcoind listreceivedbyaddress 0 true
        
        minconf: minimum number of confirmations to count
        includeempty: True/False
        """
        return self.bitcoind.listreceivedbyaddress(minconf, includeempty)
    
    def listsinceblock(self, blockhash, targetconfirmations):
        """Get all transactions in blocks since block [blockhash], or all transactions if omitted.
        
        blockhash:
        target-confirmations: 
        """
        return self.bitcoind.listsinceblock(blockhash, targetconfirmations)
    
    def listtransactions(self, account, count=10, numfrom=0):
        """Returns up to [count] most recent transactions skipping the first [from] transactions for account [account]. 
        
        account: if [account] not provided will return recent transaction from all accounts
        count: 
        from: 
        """
        return self.bitcoind.listtransactions(account, count, numfrom)
    
    def listunspent(self, minconf=1, maxconf=999999):
        """Returns array of unspent transaction inputs in the wallet.
        
        minconf: 
        maxconf: 
        """
        return self.bitcoind.listunspent(minconf, maxconf)
    
    def listlockunspent(self):
        """Returns list of temporarily unspendable outputs."""
        return self.bitcoind.listlockunspent()
    
    def lockunspent(self):
        return None
    
    def move(self, fromaccount, toaccount, minconf=1, comment=None):
        """Move from one account in your wallet to another.
        
        fromaccount: account to move from
        toaccount: account to move to
        minconf: minimum number of confirmations
        comment: optional comment        
        """
        return self.bitcoind.move(fromaccount, toaccount, minconf, comment)
    
    def sendfrom(self, fromaccount, tobitcoinaddress, amount, minconf=1, comment=None, commentto=None):
        """Will send the given amount to the given address, ensuring the account has a valid balance using [minconf] confirmations. Returns the transaction ID if successful (not in JSON object).
        
        fromaccount: account to send from
        tobitcoinaddress: address to send to
        <amount> is a real and is rounded to 8 decimal places. 
        minconf: minimum number of confirmations
        comment: optional comment
        comment-to: optional comment-to
        """
        return self.bitcoind.sendfrom(fromaccount, tobitcoinaddress, amount, minconf, comment, commentto)
    
    def sendmany(self):
        return None
    
    def sendrawtransaction(self):
        return None
    
    def sendtoaddress(self, bitcoinaddress, amount, comment=None, commentto=None):
        """Sends bitcoins to an address. Returns the transaction ID <txid> if successful.
        
        bitcoinaddress: address to send to
        amount: <amount> is a real and is rounded to 8 decimal places. 
        comment: optional comment
        comment-to: optional comment-to
        """
        return self.bitcoind.sendtoaddress(bitcoinaddress, amount, comment, commentto)
    
    def setaccount(self, bitcoinaddress, account):
        """Sets the account associated with the given address.
        
        Assigning address that is already assigned to the same account will create a new address associated with that account.
        
        bitcoinaddress: address to associate with
        account: account to associate with
        """
        return self.bitcoind.setaccount(bitcoinaddress, account)
    
    def setgenerate(self):
        return None

    def settxfee(self, amount):
        """ Sets a transaction fee.
        
        amount: <amount> is a real and is rounded to the nearest 0.00000001
        """
        return self.bitcoind.settxfee(amount)
    
    def signmessage(self, bitcoinaddress, message):
        """Sign a message with the private key of an address.
        
        bitcoinaddress: address to send message to
        message: message to send
        """
        return self.bitcoind.signmessage(bitcoinaddress, message)
    
    def signrawtransaction(self):
        return None
    
    def stop(self):
        """Stop bitcoin server."""
        return self.bitcoind.stop()
    
    def submitblock(self):
        return None
    
    def validateaddress(self, bitcoinaddress):
        """Return information about <bitcoinaddress>.
        
        bitcoinaddress: address to retrieve information about
        """
        return self.bitcoind.validateaddress(bitcoinaddress)
    
    def verifymessage(self, bitcoinaddress, signature, message):
        """Verify a signed message.
        
        bitcoinaddress: address received from
        signature: signature of message
        message: message content
        """
        return self.bitcoind.verifymessage(bitcoinaddress, signature, message)
    
    def walletlock(self):
        """	 Removes the wallet encryption key from memory, locking the wallet. 
        
        After calling this method, you will need to call walletpassphrase again 
        before being able to call any methods which require the wallet to be unlocked.
        """
        return self.bitcoind.walletlock()
    
    def walletpassphrase(self, passphrase, timeout):
        """Stores the wallet decryption key in memory for <timeout> seconds.
        
        passphrase: passphrase to decrypt wallet with
        timeout: time before key expires
        """
        return self.bitcoind.walletpassphrase(passphrase, timeout)