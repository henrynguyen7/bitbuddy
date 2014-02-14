"""
Model file for BitBuddy schema.
Defines schema for all database tables and Foreign Key relationships.

Author: Henry Nguyen (henry@bitbuddy.biz)
        Peter Lecki (peter@bitbuddy.biz)

Date:   2013-08-07
        

TODO:
* Rethink the logic behind btc_refund_address table
* createDate default value gets entered in MySQL as static datetime at time of table creation, not as CURRENT_TIMESTAMP. updateDate as well - test this to see if it's automatically updated by web2py
* id field gets created as int(11) which may be insufficient
* reference fields do not respect notnull=True during creation in MySQL
* Record representation - It is optional but recommended to specify a format representation for records
* Configure appropriate 'ondelete' actions for referenced tables.
* Indexes - Currently the DAL API does not provide a command to create indexes on tables, but this can be done using the executesql command.

Notes:
    * db connection and tables should set migrate=false to prevent 
      automatic alterations due to incorrect queries. 
    * Order of table definition matters
    
Default values of a Field constructor:
Field(name, 'string', length=None, default=None,
      required=False, requires='<default>',
      ondelete='CASCADE', notnull=False, unique=False,
      uploadfield=True, widget=None, label=None, comment=None,
      writable=True, readable=True, update=None, authorize=None,
      autodelete=False, represent=None, compute=None,
      uploadfolder=os.path.join(request.folder,'uploads'),
      uploadseparate=None,uploadfs=None)

      
FIELD TYPE              DEFAULT FIELD VALIDATORS
string	                IS_LENGTH(length) default length is 512
text	                IS_LENGTH(65536)
blob	                None
boolean	                None
integer	                IS_INT_IN_RANGE(-1e100, 1e100)
double	                IS_FLOAT_IN_RANGE(-1e100, 1e100)
decimal(n,m)	        IS_DECIMAL_IN_RANGE(-1e100, 1e100)
date	                IS_DATE()
time	                IS_TIME()
datetime	            IS_DATETIME()
password	            None
upload	                None
reference <table>       IS_IN_DB(db,table.field,format)
list:string	            None
list:integer	        None
list:reference <table>	IS_IN_DB(db,table.field,format,multiple=True)
json	                IS_JSON()
bigint	                None
big-id	                None
big-reference	        None
      
"""


db.define_table('global_settings',
    Field('btc_from_buyer_ttl', 'integer', notnull=True, length=5, default=180),  # How long a buyer has (in seconds) to send in BTC after being shown the total amount.
    Field('min_transaction_confirmations', 'integer', notnull=True, length=3, default=6),
    Field('max_batch_wait_time', 'integer', notnull=True, length=5, default=60),  # How long we wait (in seconds) for more transactions to come in before we batch them for sending to Exchange. Two reasons: 1) Save on transaction fees (mining); 2) Performance optimization
    )

db.define_table('bank',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('name', 'string', notnull=True, length=45, label='Bank Name'),
    Field('routing_number', 'integer', notnull=True, length=9, label='Bank Routing Number'),
    Field('account_number', 'integer', notnull=True, length=17, label='Your Account Number'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('user_btc_account',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('account_name', 'string', length=45, notnull=True),
    Field('name', 'string', length=45, notnull=True), # user-defined name (default should be taken from accountName)
    Field('description', 'string', length=255), # user-defined description
    Field('is_default', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1), default=1),
    Field('is_auto_exchanged', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1), default=1),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('btc_move',
    Field('user_btc_account_id_source', 'reference user_btc_account', notnull=True, ondelete='NO ACTION'),
    Field('user_btc_account_id_destination', 'reference user_btc_account', notnull=True, ondelete='NO ACTION'),
    Field('amount', 'decimal(18,8)', notnull=True),
    Field('note', 'string', length=255),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction_type',
    Field('description', 'string', notnull=True, length=45, unique=True),  # generic\exchange\merchant\refund 
    )

db.define_table('btc_transaction_status',
    Field('description', 'string', notnull=True, length=45),  # values defined in x_fixtures.py
    )


db.define_table('user_btc_address',
    Field('user_btc_account_id', 'reference user_btc_account', notnull=True, ondelete='NO ACTION'),
    Field('address', 'string', notnull=True, length=34),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction',
    Field('btc_transaction_type_id', 'reference btc_transaction_type', notnull=True, ondelete='NO ACTION'),
    Field('btc_transaction_status_id', 'reference btc_transaction_status', notnull=True, ondelete='NO ACTION'),
    Field('user_btc_address_id', 'reference user_btc_address', notnull=True, ondelete='NO ACTION'),  # This can be either source or destination of the transaction, identified by directional flag "isIncoming". 
    Field('external_btc_address', 'string', notnull=True, length=34),  # Address of external party either sending us or receiving from us, such as buyer sending our user a payment or us refunding the buyer. 
    Field('transaction_i_d', 'string', length=64),
    Field('amount', 'decimal(18,8)', notnull=True),
    Field('is_confirmed', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1), default=0),
    Field('is_incoming', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1)),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction_status_history',
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    Field('btc_transaction_status_id', 'reference btc_transaction_status', notnull=True, ondelete='NO ACTION'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('btc_move_to_btc_transaction',
    Field('btc_move_id', 'reference btc_move', notnull=True, ondelete='NO ACTION'),
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    )

db.define_table('exchange',
    Field('name', 'string', notnull=True, length=45),
    Field('web_url', 'string', notnull=True, length=255),
    Field('api_url', 'string', notnull=True, length=255),
    Field('username', 'string', notnull=True, length=255),
    Field('password', 'string', notnull=True, length=45),
    Field('api_key', 'string', length=45),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('exchange_quote',
    # There is a circular reference on ForeignKeys here and should be rewritten - there's already a note about that in the btcTransactionStatus table
    Field('btc_transaction_merchant_id', 'reference btc_transaction_merchant', notnull=True, ondelete='NO ACTION'),
    Field('exchange_id', 'reference exchange', notnull=True, ondelete='NO ACTION'),
    Field('exchange_rate', 'decimal(12,2)', notnull=True),  # USD per BTC 
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('exchange_btc_deposit_address',
    Field('exchange_id', 'reference exchange', notnull=True, ondelete='NO ACTION'),
    Field('address', 'string', notnull=True, length=34),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('exchange_btc_deposit_address_has_btc_transaction',
    Field('exchange_btc_deposit_address_id', 'reference exchange_btc_deposit_address', notnull=True, ondelete='NO ACTION'),  # Is this necessary? It's really not a m:m relationship. Does it improve query performance if asking for all transactions sent to a particular exchange? Or would indexing the externalBtcAddress column and querying all btcTransactions where externalBtcAddress is in subselect be just as good and reduce the schema complexity. /* comment truncated */
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    )

db.define_table('exchange_fee',
    Field('exchange_id', 'reference exchange', notnull=True, ondelete='NO ACTION'),
    Field('sell', 'decimal(12,2)', notnull=True),
    Field('is_sell_percent', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1)),  # Otherwise it's a constant/static amount.
    Field('buy', 'decimal(12,2)', notnull=True),
    Field('is_buy_percent', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1)),
    Field('withdraw', 'decimal(12,2)', notnull=True),
    Field('is_withdraw_percent', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1)),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('request_type',
    Field('description', 'string', notnull=True, length=45),  # order\withdraw 
    )

db.define_table('order_type',
    Field('description', 'string', notnull=True, length=45),  # buy\sell 
    )

db.define_table('exchange_request',
    Field('exchange_id', 'reference exchange', notnull=True, ondelete='NO ACTION'),
    Field('request_type_id', 'reference request_type', notnull=True, ondelete='NO ACTION'),
    Field('request_i_d', 'string', length=45),
    Field('confirmation_i_d', 'string', length=45),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('exchange_request_order',
    Field('exchange_request_id', 'reference exchange_request', notnull=True, ondelete='NO ACTION'),
    Field('order_type_id', 'reference order_type', notnull=True, ondelete='NO ACTION'),
    Field('btc_qty', 'decimal(18,8)', notnull=True),
    Field('rate', 'decimal(12,2)', notnull=True),
    Field('fee_rate', 'decimal(12,2)', notnull=True),
    Field('is_fee_percent', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1)),
    Field('fee_amount', 'decimal(12,2)'),
    Field('total_amount', 'decimal(12,2)'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('exchange_request_withdraw',
    Field('exchange_request_id', 'reference exchange_request', notnull=True, ondelete='NO ACTION'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('anon_buyer',
    Field('email', 'string', notnull=True, length=255),
    Field('refund_address', 'string', notnull=True, length=34),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('btc_refund_address',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('refund_address', 'string', notnull=True, length=34),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('merchant_info',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('company_name', 'string', length=255),
	Field('website', 'string', length=255),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction_merchant',
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    Field('anon_buyer_id', 'reference anon_buyer', notnull=True, ondelete='NO ACTION'),
    Field('exchange_quote_id', 'reference exchange_quote', notnull=True, ondelete='NO ACTION'),
    Field('exchange_quote_padding', 'decimal(12,2)', notnull=True, default='0.00'),  # Exchange rate might be padded if we see a down trend so that we don't have to reverse transactions. 
    Field('total_expected_btc', 'decimal(18,8)', notnull=True),
    Field('amount_received_btc', 'decimal(18,8)'),
    Field('date_received', 'datetime'),
    Field('is_refunded', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1), default=0),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction_exchange',
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    Field('is_available', 'integer', notnull=True, requires=IS_INT_IN_RANGE(0,1), default=0),  # Exchange confirmed this transaction as available for trading. 
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction_generic',
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('btc_transaction_refund',
    Field('btc_transaction_id', 'reference btc_transaction', notnull=True, ondelete='NO ACTION'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('order_detail', 
	# Move items from btcTransactionMerchant here that relate to orders, so that we can have Moves fund orders as well. \nAgain problem with two parents though.
    Field('btc_transaction_merchant_id', 'reference btc_transaction_merchant', notnull=True, ondelete='NO ACTION'),
    Field('btc_move_id', 'reference btc_move', notnull=True, ondelete='NO ACTION'),
    Field('product_name', 'string', notnull=True, length=45),
    Field('product_description', 'string', length=255),
    Field('quantity', 'integer', notnull=True, length=10),
    Field('price_per_product_usd', 'decimal(12,2)', notnull=True),
    Field('shipping_cost_usd', 'decimal(12,2)', notnull=True, default='0.00'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )

db.define_table('phone_type',
    Field('description', 'string', notnull=True, length=45),  # home\office\mobile 
    )

db.define_table('phone',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('phone_type_id', 'reference phone_type', notnull=True, ondelete='NO ACTION', label='Phone Type'),
    Field('number', 'integer', notnull=True, length=10, label='Phone Number'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False),
    )

db.define_table('physical_address_type',
    Field('description', 'string', notnull=True, length=45),  # shipping\billing\both 
    )

db.define_table('physical_address',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('physical_address_type_id', 'reference physical_address_type', notnull=True, ondelete='NO ACTION', label='Address Type'),
    Field('street_number', 'integer', notnull=True, length=8, label='Street Number'),
    Field('street_name', 'string', notnull=True, length=100, label='Street Name'),
    Field('unit_number', 'string', length=10, label='Apt/Suite/Unit #'),
    Field('city', 'string', notnull=True, length=45, label='City'),
    Field('state', 'string', notnull=True, length=2, label='State'),
    Field('country', 'string', notnull=True, length=45, label='Country'),
    Field('description', 'string', length=45, label='Description/Note'),  # User defined description of this address.
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=True, writable=False, label='Address added on'),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=True, writable=False, label='Last updated on'),
    )

db.define_table('product',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('number', 'string', length=45, label='Product Number', comment='(optional)'),
    Field('name', 'string', notnull=True, length=45, label='Product Name'),
    Field('description', 'string', length=255, label='Product Description'),
    Field('price_usd', 'decimal(12,2)', notnull=True, label='Price in USD'),
    #Field('price_btc', 'decimal(18,8)'),  # NOT SURE WHY THIS WAS ADDED 
    Field('shipping_cost', 'decimal(12,2)', notnull=True, default='0.00', label='Shipping Cost', comment='Leave blank for free shipping'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=True, writable=False, label='Product added on'),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=True, writable=False, label='Last updated on'),
    )

db.define_table('user_status',
    Field('description', 'string', notnull=True, length=45),
    )

db.define_table('user_status_history',
    Field('auth_user_id', 'reference auth_user', notnull=True, ondelete='NO ACTION'),
    Field('user_status_id', 'reference user_status', notnull=True, ondelete='NO ACTION'),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    )
