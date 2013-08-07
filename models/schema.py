legacy_db = DAL('mysql://temproot:@localhost/bitbuddy2', migrate=False)

legacy_db.define_table('bank', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('user_id', 'integer', notnull=True),  # (`user_id` bigint(20) unsigned NOT NULL,)
    Field('name', 'string', notnull=True),     # (`name` varchar(45) NOT NULL,)
    Field('routingNumber', 'integer', notnull=True),  # (`routingNumber` int(9) unsigned NOT NULL,)
    Field('accountNumber', 'integer', notnull=True),  # (`accountNumber` bigint(17) unsigned NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('bankAccount', 
    Field('id', 'integer', notnull=True),      # (`id` int(11) NOT NULL,)
    Field('number', 'integer'),                # (`number` int(11) DEFAULT NULL,)
    )

legacy_db.define_table('btcMove', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('userBtcAccount_id_source', 'integer', notnull=True),  # (`userBtcAccount_id_source` bigint(20) unsigned NOT NULL,)
    Field('userBtcAccount_id_destination', 'integer', notnull=True),  # (`userBtcAccount_id_destination` bigint(20) unsigned NOT NULL,)
    Field('amount', 'integer', notnull=True),  # (`amount` decimal(10,8) unsigned NOT NULL,)
    Field('note', 'string'),                   # (`note` varchar(255) DEFAULT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('btcMove_to_btcTransaction', 
    Field('id', 'id', notnull=True),           # This column is technically not necessary, but has to exist for web2py compatibility with conversion scripts.  (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'This column is technically not necessary, but has to exist for web2py compatibility with conversion scripts.',)
    Field('btcMove_id', 'integer', notnull=True),  # (`btcMove_id` bigint(20) unsigned NOT NULL,)
    Field('btcTransaction_id', 'integer', notnull=True),  # (`btcTransaction_id` bigint(20) unsigned NOT NULL,)
    )

legacy_db.define_table('btcTransaction', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcTransactionType_id', 'integer', notnull=True),  # (`btcTransactionType_id` bigint(20) unsigned NOT NULL,)
    Field('transactionStatus_id', 'integer', notnull=True),  # (`transactionStatus_id` bigint(20) unsigned NOT NULL,)
    Field('userBtcAddress_id', 'integer', notnull=True),  # This can be either source or destination of the transaction, identified by directional flag "isIncoming".  (`userBtcAddress_id` bigint(20) unsigned NOT NULL COMMENT 'This can be either source or destination of the transaction, identified by directional flag "isIncoming".',)
    Field('externalBtcAddress', 'string', notnull=True),  # Address of external party either sending us or receiving from us, such as buyer sending our user a payment or us refunding the buyer.  (`externalBtcAddress` varchar(34) NOT NULL COMMENT 'Address of external party either sending us or receiving from us, such as buyer sending our user a payment or us refunding the buyer.',)
    Field('transactionID', 'string'),          # (`transactionID` char(64) DEFAULT NULL,)
    Field('amount', 'integer', notnull=True),  # (`amount` decimal(10,8) unsigned NOT NULL,)
    Field('isConfirmed', 'integer', notnull=True),  # (`isConfirmed` tinyint(1) NOT NULL DEFAULT '0',)
    Field('isIncoming', 'integer', notnull=True),  # (`isIncoming` tinyint(1) NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('btcTransactionExchange', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcTransaction_id', 'integer', notnull=True),  # (`btcTransaction_id` bigint(20) unsigned NOT NULL,)
    Field('isAvailable', 'integer', notnull=True),  # Exchange confirmed this transaction as available for trading.  (`isAvailable` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Exchange confirmed this transaction as available for trading.',)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('btcTransactionGeneric', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcTransaction_id', 'integer', notnull=True),  # (`btcTransaction_id` bigint(20) unsigned NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('btcTransactionMerchant', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcTransaction_id', 'integer', notnull=True),  # (`btcTransaction_id` bigint(20) unsigned NOT NULL,)
    Field('userBuyer_id', 'integer', notnull=True),  # (`userBuyer_id` bigint(20) unsigned NOT NULL,)
    Field('exchangeQuote_id', 'integer', notnull=True),  # (`exchangeQuote_id` bigint(20) unsigned NOT NULL,)
    Field('exchangeQuotePadding', 'integer', notnull=True),  # Exchange rate might be padded if we see a down trend so that we don''t have to reverse transactions.  (`exchangeQuotePadding` decimal(10,2) unsigned NOT NULL DEFAULT '0.00' COMMENT 'Exchange rate might be padded if we see a down trend so that we don''t have to reverse transactions.',)
    Field('totalExpectedBtc', 'integer', notnull=True),  # (`totalExpectedBtc` decimal(10,8) unsigned NOT NULL,)
    Field('amountReceivedBtc', 'integer'),     # (`amountReceivedBtc` decimal(10,8) unsigned DEFAULT NULL,)
    Field('dateReceived', 'datetime'),         # (`dateReceived` timestamp NULL DEFAULT NULL,)
    Field('isRefunded', 'integer', notnull=True),  # (`isRefunded` tinyint(1) NOT NULL DEFAULT '0',)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('btcTransactionRefund', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcTransaction_id', 'integer', notnull=True),  # (`btcTransaction_id` bigint(20) unsigned NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('btcTransactionType', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('description', 'string', notnull=True),  # generic\nexchange\nmerchant\nrefund  (`description` varchar(45) NOT NULL COMMENT 'generic\nexchange\nmerchant\nrefund',)
    )

legacy_db.define_table('exchange', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('name', 'string', notnull=True),     # (`name` varchar(45) NOT NULL,)
    Field('webUrl', 'string', notnull=True),   # (`webUrl` varchar(255) NOT NULL,)
    Field('apiUrl', 'string', notnull=True),   # (`apiUrl` varchar(255) NOT NULL,)
    Field('username', 'string', notnull=True),  # (`username` varchar(255) NOT NULL,)
    Field('password', 'string', notnull=True),  # (`password` varchar(45) NOT NULL,)
    Field('apiKey', 'string'),                 # (`apiKey` varchar(255) DEFAULT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('exchangeBtcDepositAddress', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('exchange_id', 'integer', notnull=True),  # (`exchange_id` bigint(20) unsigned NOT NULL,)
    Field('address', 'string', notnull=True),  # (`address` varchar(34) NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('exchangeBtcDepositAddress_has_btcTransaction', 
    Field('id', 'id', notnull=True),           # This column is technically not necessary, but has to exist for web2py compatibility with conversion scripts.  (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'This column is technically not necessary, but has to exist for web2py compatibility with conversion scripts.',)
    Field('exchangeBtcDepositAddress_id', 'integer', notnull=True),  # Is this necessary? It''s really not a m:m relationship.\nDoes it improve query performance if asking for all transactions sent to a particular exchange? \nOr would indexing the externalBtcAddress column and querying all btcTransactions where externalBtcAddre /* comment truncated */ /*ss is in subselect be just as good and reduce the schema complexity. */  (`exchangeBtcDepositAddress_id` bigint(20) unsigned NOT NULL COMMENT 'Is this necessary? It''s really not a m:m relationship.\nDoes it improve query performance if asking for all transactions sent to a particular exchange? \nOr would indexing the externalBtcAddress column and querying all btcTransactions where externalBtcAddre /* comment truncated */ /*ss is in subselect be just as good and reduce the schema complexity. */',)
    Field('btcTransaction_id', 'integer', notnull=True),  # (`btcTransaction_id` bigint(20) unsigned NOT NULL,)
    )

legacy_db.define_table('exchangeFee', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('exchange_id', 'integer', notnull=True),  # (`exchange_id` bigint(20) unsigned NOT NULL,)
    Field('sell', 'integer', notnull=True),    # (`sell` decimal(10,2) unsigned NOT NULL,)
    Field('isSellPercent', 'integer', notnull=True),  # otherwise constant/static amount  (`isSellPercent` tinyint(1) NOT NULL COMMENT 'otherwise constant/static amount',)
    Field('buy', 'integer', notnull=True),     # (`buy` decimal(10,2) unsigned NOT NULL,)
    Field('isBuyPercent', 'integer', notnull=True),  # (`isBuyPercent` tinyint(1) NOT NULL,)
    Field('withdraw', 'integer', notnull=True),  # (`withdraw` decimal(10,2) unsigned NOT NULL,)
    Field('isWithdrawPercent', 'integer', notnull=True),  # (`isWithdrawPercent` tinyint(1) NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('exchangeQuote', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcTransactionMerchant_id', 'integer', notnull=True),  # (`btcTransactionMerchant_id` bigint(20) unsigned NOT NULL,)
    Field('exchange_id', 'integer', notnull=True),  # (`exchange_id` bigint(20) unsigned NOT NULL,)
    Field('exchangeRate', 'integer', notnull=True),  # USD per BTC  (`exchangeRate` decimal(10,2) unsigned NOT NULL COMMENT 'USD per BTC',)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('exchangeRequest', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('exchange_id', 'integer', notnull=True),  # (`exchange_id` bigint(20) unsigned NOT NULL,)
    Field('requestType_id', 'integer', notnull=True),  # (`requestType_id` bigint(20) unsigned NOT NULL,)
    Field('requestID', 'string'),              # (`requestID` varchar(45) DEFAULT NULL,)
    Field('confirmationID', 'string'),         # (`confirmationID` varchar(45) DEFAULT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('exchangeRequestOrder', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('exchangeRequest_id', 'integer', notnull=True),  # (`exchangeRequest_id` bigint(20) unsigned NOT NULL,)
    Field('orderType_id', 'integer', notnull=True),  # (`orderType_id` bigint(20) unsigned NOT NULL,)
    Field('btcQty', 'integer', notnull=True),  # (`btcQty` decimal(10,8) unsigned NOT NULL,)
    Field('rate', 'integer', notnull=True),    # (`rate` decimal(10,2) unsigned NOT NULL,)
    Field('feeRate', 'integer', notnull=True),  # (`feeRate` decimal(10,2) unsigned NOT NULL,)
    Field('isFeePercent', 'integer', notnull=True),  # (`isFeePercent` tinyint(1) NOT NULL,)
    Field('feeAmount', 'integer'),             # (`feeAmount` decimal(10,2) unsigned DEFAULT NULL,)
    Field('totalAmount', 'integer'),           # (`totalAmount` decimal(10,2) unsigned DEFAULT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('exchangeRequestWithdraw', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('exchangeRequest_id', 'integer', notnull=True),  # (`exchangeRequest_id` bigint(20) unsigned NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('globalSettings', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('btcFromBuyerTTL', 'integer', notnull=True),  # How long a buyer has (in seconds) to send in BTC after being shown the total amount.  (`btcFromBuyerTTL` smallint(5) unsigned NOT NULL DEFAULT '180' COMMENT 'How long a buyer has (in seconds) to send in BTC after being shown the total amount.',)
    Field('minTransactionConfirmations', 'integer', notnull=True),  # (`minTransactionConfirmations` tinyint(3) unsigned NOT NULL DEFAULT '6',)
    Field('maxBatchWaitTime', 'integer', notnull=True),  # How long we wait (in seconds) for more transactions to come in before we batch them for sending to Exchange.\nTwo reasons:\n   1) Save on transaction fees (mining)\n   2) Performance optimization  (`maxBatchWaitTime` smallint(5) unsigned NOT NULL DEFAULT '60' COMMENT 'How long we wait (in seconds) for more transactions to come in before we batch them for sending to Exchange.\nTwo reasons:\n   1) Save on transaction fees (mining)\n   2) Performance optimization',)
    )

legacy_db.define_table('orderDetail', 
    Field('id', 'integer', notnull=True),      # Move items from btcTransactionMerchant here that relate to orders, so that we can have Moves fund orders as well. \nAgain problem with two parents though.  (`id` bigint(20) unsigned NOT NULL COMMENT 'Move items from btcTransactionMerchant here that relate to orders, so that we can have Moves fund orders as well. \nAgain problem with two parents though.',)
    Field('btcTransactionMerchant_id', 'integer', notnull=True),  # (`btcTransactionMerchant_id` bigint(20) unsigned NOT NULL,)
    Field('btcMove_id', 'integer', notnull=True),  # (`btcMove_id` bigint(20) unsigned NOT NULL,)
    Field('productName', 'string', notnull=True),  # (`productName` varchar(45) NOT NULL,)
    Field('productDescription', 'string'),     # (`productDescription` varchar(255) DEFAULT NULL,)
    Field('quantity', 'integer', notnull=True),  # (`quantity` int(10) unsigned NOT NULL,)
    Field('pricePerProductUsd', 'integer', notnull=True),  # (`pricePerProductUsd` decimal(10,2) unsigned NOT NULL,)
    Field('shippingCostUsd', 'integer', notnull=True),  # (`shippingCostUsd` decimal(10,2) unsigned NOT NULL DEFAULT '0.00',)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('orderType', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('description', 'string'),            # buy\nsell  (`description` varchar(45) DEFAULT NULL COMMENT 'buy\nsell',)
    )

legacy_db.define_table('phone', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) NOT NULL AUTO_INCREMENT,)
    Field('user_id', 'integer', notnull=True),  # (`user_id` bigint(20) unsigned NOT NULL,)
    Field('phoneType_id', 'integer', notnull=True),  # (`phoneType_id` bigint(20) unsigned NOT NULL,)
    Field('number', 'integer', notnull=True),  # (`number` int(10) unsigned NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('phoneType', 
    Field('id', 'integer', notnull=True),      # (`id` bigint(20) unsigned NOT NULL,)
    Field('description', 'string', notnull=True),  # home\noffice\nmobile  (`description` varchar(45) NOT NULL COMMENT 'home\noffice\nmobile',)
    )

legacy_db.define_table('physicalAddress', 
    Field('id', 'integer', notnull=True),      # (`id` bigint(20) unsigned NOT NULL,)
    Field('user_id', 'integer', notnull=True),  # (`user_id` bigint(20) unsigned NOT NULL,)
    Field('physicalAddressType_id', 'integer', notnull=True),  # (`physicalAddressType_id` bigint(20) unsigned NOT NULL,)
    Field('streetNumber', 'integer', notnull=True),  # (`streetNumber` mediumint(8) unsigned NOT NULL,)
    Field('streetName', 'string', notnull=True),  # (`streetName` varchar(100) NOT NULL,)
    Field('unitNumber', 'string'),             # (`unitNumber` varchar(10) DEFAULT NULL,)
    Field('city', 'string', notnull=True),     # (`city` varchar(45) NOT NULL,)
    Field('state', 'string', notnull=True),    # (`state` char(2) NOT NULL,)
    Field('country', 'string', notnull=True),  # (`country` varchar(45) NOT NULL,)
    Field('description', 'string'),            # user defined description of address  (`description` varchar(45) DEFAULT NULL COMMENT 'user defined description of address',)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('physicalAddressType', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('description', 'string', notnull=True),  # shipping\nbilling\nboth  (`description` varchar(45) NOT NULL COMMENT 'shipping\nbilling\nboth',)
    )

legacy_db.define_table('product', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('userMerchant_id', 'integer', notnull=True),  # (`userMerchant_id` bigint(20) unsigned NOT NULL,)
    Field('number', 'string'),                 # (`number` varchar(45) DEFAULT NULL,)
    Field('name', 'string', notnull=True),     # (`name` varchar(45) NOT NULL,)
    Field('description', 'string'),            # (`description` varchar(255) DEFAULT NULL,)
    Field('priceUSD', 'integer', notnull=True),  # (`priceUSD` decimal(10,2) unsigned NOT NULL,)
    Field('priceBTC', 'integer'),              # NOT SURE WHY THIS WAS ADDED  (`priceBTC` decimal(10,8) unsigned DEFAULT NULL COMMENT 'NOT SURE WHY THIS WAS ADDED',)
    Field('shippingCost', 'integer', notnull=True),  # (`shippingCost` decimal(10,2) unsigned NOT NULL DEFAULT '0.00',)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('requestType', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('description', 'string', notnull=True),  # order\nwithdraw  (`description` varchar(45) NOT NULL COMMENT 'order\nwithdraw',)
    )

legacy_db.define_table('transactionStatus', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('description', 'string', notnull=True),  # RETHINK THIS\ntransactionStatus\n    (refund)\n         	confirmed\n	invalid\n                sent\n     (merchant)\n                notBroadcast\n	receivedFull\n	receivedShort\n	receivedOver\n	receivedFullLate\n	receivedShortLate\n	receivedOverLate\n	expired\n	confirme /* comment truncated */ /*d\n	invalid\n                sent\n	\n	handle failure cases such as receivedShort and confirmed by network*/  (`description` varchar(45) NOT NULL COMMENT 'RETHINK THIS\ntransactionStatus\n    (refund)\n         	confirmed\n	invalid\n                sent\n     (merchant)\n                notBroadcast\n	receivedFull\n	receivedShort\n	receivedOver\n	receivedFullLate\n	receivedShortLate\n	receivedOverLate\n	expired\n	confirme /* comment truncated */ /*d\n	invalid\n                sent\n	\n	handle failure cases such as receivedShort and confirmed by network*/',)
    )

legacy_db.define_table('user', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('userStatus_id', 'integer', notnull=True),  # (`userStatus_id` bigint(20) unsigned NOT NULL,)
    Field('loginEmail', 'string', notnull=True),  # (`loginEmail` varchar(255) NOT NULL,)
    Field('password', 'string', notnull=True),  # (`password` varchar(45) NOT NULL,)
    Field('firstName', 'string', notnull=True),  # (`firstName` varchar(45) NOT NULL,)
    Field('lastName', 'string', notnull=True),  # (`lastName` varchar(45) NOT NULL,)
    Field('lastLoginDate', 'datetime', notnull=True),  # (`lastLoginDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('userBtcAddress', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('userBtcAccount_id', 'integer', notnull=True),  # (`userBtcAccount_id` bigint(20) unsigned NOT NULL,)
    Field('address', 'string', notnull=True),  # (`address` varchar(34) NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('userBuyer', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('user_id', 'integer', notnull=True),  # (`user_id` bigint(20) unsigned NOT NULL,)
    Field('email', 'string', notnull=True),    # (`email` varchar(255) NOT NULL,)
    Field('refundAddress', 'string', notnull=True),  # (`refundAddress` varchar(34) NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('userMerchant', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('user_id', 'integer', notnull=True),  # (`user_id` bigint(20) unsigned NOT NULL,)
    Field('website', 'string'),                # (`website` varchar(255) DEFAULT NULL,)
    Field('company', 'string'),                # (`company` varchar(255) DEFAULT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    Field('updateDate', 'datetime', notnull=True),  # (`updateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,)
    )

legacy_db.define_table('userStatus', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('description', 'string', notnull=True),  # (`description` varchar(45) NOT NULL,)
    )

legacy_db.define_table('userStatusHistory', 
    Field('id', 'id', notnull=True),           # (`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,)
    Field('user_id', 'integer', notnull=True),  # (`user_id` bigint(20) unsigned NOT NULL,)
    Field('userStatus_id', 'integer', notnull=True),  # (`userStatus_id` bigint(20) unsigned NOT NULL,)
    Field('createDate', 'datetime', notnull=True),  # (`createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,)
    )
