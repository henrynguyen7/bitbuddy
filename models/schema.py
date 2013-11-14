"""
Model file for BitBuddy schema.

Defines schema for all database tables and Foreign Key relationships.

Note: db connection and tables should set migrate=false to prevent 
automatic alterations due to incorrect queries. 
E.g.: db = DAL('sqlite://storage.db', migrate=False)

Note: Order of table definition matters

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

########################################################################
# Reference: valid web2py field types
# field type	            default field validators
# string	                IS_LENGTH(length) default length is 512
# text	                IS_LENGTH(65536)
# blob	                None
# boolean	                None
# integer	                IS_INT_IN_RANGE(-1e100, 1e100)
# double	                IS_FLOAT_IN_RANGE(-1e100, 1e100)
# decimal(n,m)	        IS_DECIMAL_IN_RANGE(-1e100, 1e100)
# date	                IS_DATE()
# time	                IS_TIME()
# datetime	            IS_DATETIME()
# password	            None
# upload	                None
# reference <table>	    IS_IN_DB(db,table.field,format)
# list:string	            None
# list:integer	        None
# list:reference <table>	IS_IN_DB(db,table.field,format,multiple=True)
# json	                IS_JSON()
# bigint	                None
# big-id	                None
# big-reference	        None
########################################################################

# TODO: Modify default field values as needed. Defaults are below.
# Field(name, 'string', length=None, default=None,
#       required=False, requires='<default>',
#       ondelete='CASCADE', notnull=False, unique=False,
#       uploadfield=True, widget=None, label=None, comment=None,
#       writable=True, readable=True, update=None, authorize=None,
#       autodelete=False, represent=None, compute=None,
#       uploadfolder=os.path.join(request.folder,'uploads'),
#       uploadseparate=None,uploadfs=None)

db.define_table('bank',
                Field('auth_user_id', 'reference auth_user'),
                Field('name', 'string'),
                Field('routingNumber', 'string'),
                Field('accountNumber', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='bank.table')

db.define_table('userBtcAccount',
                Field('auth_user_id', 'reference auth_user', notnull=True),
                Field('accountName', 'string'),
                Field('name', 'string'),
                Field('description', 'string'),
                Field('isDefault', 'boolean'),
                Field('isAutoExchanged', 'boolean'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='userBtcAccount.table')

db.define_table('btcMove',
                Field('userBtcAccount_id_source', 'reference userBtcAccount'),
                Field('userBtcAccount_id_destination', 'reference userBtcAccount'),
                Field('amount', 'double'),
                Field('note', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='btcMove.table')

db.define_table('btcTransactionType',
                Field('description', 'string', notnull=True),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='btcTransactionType.table')

# TODO: This table's values need to be prepopulated
db.define_table('transactionStatus',
                Field('description', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='transactionStatus.table')

db.define_table('btcTransaction',
                Field('btcTransactionType_id', 'reference btcTransactionType', notnull=True),
                Field('transactionStatus_id', 'reference transactionStatus', notnull=True),
                Field('transactionId', 'integer'),
                Field('sourceAddress', 'string'),    
                Field('destinationAddress', 'string'),
                Field('isConfirmed', 'boolean'),
                Field('isIncoming', 'boolean'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='btcTransaction.table')

db.define_table('btcTransactionExchange',
                Field('btcTransaction_id', 'reference btcTransaction', notnull=True),
                Field('createDate', 'date'))
                # primarykey=['id'],
                # migrate='btcTransactionExchange.table')

db.define_table('btcTransactionGeneric',
                Field('btcTransaction_id', 'reference btcTransaction', notnull=True),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='btcTransactionGeneric.table')

db.define_table('buyer',
                Field('email', 'string'),
                # TODO: Clarify what other_contact_info is
                Field('other_contact_info', 'string'),
                Field('refundAddress', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='buyer.table')

db.define_table('btcTransactionMerchant',
                Field('btcTransaction_id', 'reference btcTransaction', notnull=True),
                Field('buyer_id', 'reference buyer', notnull=True),
                Field('productName', 'string'),
                Field('productDescription', 'string'),
                Field('quantity', 'integer'),
                Field('pricePer', 'double'),
                Field('shippingCost', 'double'),
                Field('totalExpected', 'double'),
                Field('amountReceived', 'double'),
                Field('isRefunded', 'boolean'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='btcTransactionMerchant.table')

db.define_table('btcTransactionRefund',
                Field('btcTransaction_id', 'reference btcTransaction', notnull=True),
                Field('createDate', 'date'))
                # primarykey=['id'],
                # migrate='btcTransactionRefund.table')

# TODO: This table's values need to be prepopulated
db.define_table('exchange',
                Field('name', 'string'),
                Field('webUrl', 'string'),
                Field('apiUrl', 'string'),
                Field('username', 'string'),
                Field('password', 'string'),
                Field('apiKey', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchange.table')

# TODO: This table's values need to be prepopulated
db.define_table('exchangeBtcDepositAddress',
                Field('exchange_id', 'reference exchange', notnull=True),
                Field('address', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchangeBtcDepositAddress.table')

db.define_table('exchangeBtcDepositAddress_has_btcTransaction',
                Field('exchangeBtcDepositAddress_id', 'reference exchangeBtcDepositAddress', notnull=True),
                Field('btcTransaction_id', 'reference btcTransaction', notnull=True),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchangeBtcDepositAddress_has_btcTransaction.table')

# TODO: This table's values need to be prepopulated
db.define_table('exchangeFee',
                Field('exchange_id', 'reference exchange', notnull=True),
                Field('sell', 'double'),
                Field('isSellPercent', 'boolean'),
                Field('buy', 'double'),
                Field('isBuyPercent', 'boolean'),
                Field('withdraw', 'double'),
                Field('isWithdrawPercent', 'boolean'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchangeFee.table')

# TODO: This table's values need to be prepopulated
db.define_table('requestType',
                Field('description', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='requestType.table')

db.define_table('exchangeRequest',
                Field('exchange_id', 'reference exchange', notnull=True),
                Field('requestType_id', 'reference requestType', notnull=True),
                Field('requestId', 'string'),
                Field('confirmationId', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchangeRequest.table')

# TODO: This table's values need to be prepopulated
db.define_table('orderType',
                Field('description', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='orderType.table')

db.define_table('exchangeRequestOrder',
                Field('exchangeRequest_id', 'reference exchangeRequest', notnull=True),
                Field('orderType_id', 'reference orderType', notnull=True),
                Field('btcQuantity', 'double'),
                # TODO: Add currency table and use FK instead
                Field('currency', 'string'),
                Field('rate', 'double'),
                Field('feeRate', 'double'),
                Field('isFeePercent', 'boolean'),
                Field('feeAmount', 'double'),
                Field('totalAmount', 'double'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchangeRequestOrder.table')


db.define_table('exchangeRequestWithdraw',
                Field('exchangeRequest_id', 'reference exchangeRequest', notnull=True),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='exchangeRequestWithdraw.table')

# TODO: This table's values need to be prepopulated
db.define_table('globalSettings',
                Field('btcAddressTTL', 'integer'),
                Field('minTransactionConfirmations', 'integer'),
                Field('maxBatchWaitTimeMilliseconds', 'integer'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='globalSettings.table')

db.define_table('merchantProduct',
                Field('auth_user_id', 'reference auth_user', notnull=True, writable=False, readable=False),
                Field('merchantNumber', 'string'),
                Field('name', 'string'),
                Field('description', 'string'),
                Field('priceUSD', 'double'),
                Field('priceBTC', 'double'),
                Field('shippingCost', 'double'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='merchantProduct.table')

# TODO: User table may not be needed if we're using built-in Auth.user
# db.define_table('bitbuddyUser',
#                 Field('email','string'),
#                 Field('passwordHash', 'string'),
#                 Field('isActive', 'boolean'),
#                 Field('firstName', 'string'),
#                 Field('lastName', 'string'),
#                 Field('company', 'string'),
#                 Field('website', 'string'),
#                 Field('lastLoginDate', 'date'),
#                 Field('createDate', 'datetime', default=request.now))
#                 # primarykey=['id'],
#                 # migrate='bitbuddyUser.table')

db.define_table('userBtcAddress',
                Field('userBtcAccount_id', 'reference userBtcAccount', notnull=True),
                Field('address', 'string'),
                Field('createDate', 'datetime', default=request.now))
                # primarykey=['id'],
                # migrate='userBtcAddress.table')