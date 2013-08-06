"""
BitBuddy Fixtures (seed data)

More info: http://thadeusb.com/weblog/2010/4/21/using_fixtures_in_web2py
"""

# Set RESET = TRUE to reset ALL database data
# Useful for dev/testing... don't let this anywhere near production
RESET = False

if RESET:
    for table in db.tables():
        db[table].drop()
    db.commit()

if db(db.auth_user.id > 0).count() == 0:
    db.auth_user.insert(
        first_name='Testers',
        last_name='Inc',
        email='test@bitbuddy.com',
        password='<include a pre-encrypted password here>')

if db(db.exchange.id > 0).count() == 0:
    db.exchange.insert(
        name='Test',
        webUrl='http://www.test.com',
        apiUrl='http://www.test.com',
        username='test',
        password='test',
        apiKey='test')

if db(db.exchangeFee.id > 0).count() == 0:
    db.exchangeFee.insert(
        exchange_id=01,
        sell=01,
        isSellPercent=False,
        buy=01,
        isBuyPercent=False,
        withdraw=01,
        isWithdrawPercent=False)

if db(db.globalSettings.id > 0).count() == 0:
    db.globalSettings.insert(
        btcAddressTTL=1000,
        minTransactionConfirmations=01,
        maxBatchWaitTimeMilliseconds=60)

if db(db.orderType.id > 0).count() == 0:
    db.orderType.insert(
        id=01,
        description='test1')

if db(db.requestType.id > 0).count() == 0:
    db.requestType.insert(
        id=01,
        description='test1')

if db(db.transactionStatus.id > 0).count() == 0:
    db.transactionStatus.insert(
        id=01,
        description='test1')