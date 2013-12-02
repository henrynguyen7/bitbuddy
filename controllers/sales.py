"""

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

from gluon.custom_import import track_changes
from gluon.tools import Crud

# Runs all modules with the latest changes instead of cached version, useful for dev
track_changes(True)

crud = Crud(db)

def sales():
    grid = SQLFORM.grid(
        query=db.merchantProduct.auth_user_id==request.vars.auth_user_id,
        fields=[
            db.merchantProduct.name,
            db.merchantProduct.description,
            db.merchantProduct.priceUSD],
        deletable=False,
        editable=False,
        details=False,
        selectable=None,
        searchable=False,
        # Take user to createBuyer page first instead of directly to purchaseProduct page. TODO: allow login if already existing.
        # links=[lambda row: A(T('Purchase'),_href=URL("sales","purchaseProduct",vars={'productId': row.id}))],
        links=[lambda row: A(T('Purchase'),_href=URL("sales","createBuyerAccount",vars=dict(productId=row.id)))],
        links_in_grid=True,
        user_signature=True,
        csv=False,
        headers={
            'merchantProduct.name': 'Product Name',
            'merchantProduct.description': 'Description',
            'merchantProduct.priceUSD': 'Price (USD)'})
    grid.element('.web2py_counter', replace=None)
    return dict(grid=grid)

def createBuyerAccount():
    # TODO: modify to create a new auth_user of type "buyer" instead of inputting an entry directly into the buyer table.
    form = SQLFORM(db.buyer)
    if form.process().accepted:
        redirect(URL('purchaseProduct', vars=dict(buyerId=form.vars.id, productId=request.vars.productId)))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def purchaseProduct():
    """
    TODO: should perform the following functions:
    1. Generate new bitcoin address
    1a. Add bitcoin address and account to userBtcAddress and userBtcAccount tables
    2. Query exchange for latest exchange rate
    3. Calculate priceBTC of Product
    4. Display popup page with:
        - 10 minute timer
        - product info
        - priceBTC
        - bitcoin address to send to

    In separate function, OnBitcoinsReceivedInAddress(address)
    1. Perform calculations to determine whether payment is valid.
    2. etc...
    """
    from bitcoin_client import BitcoinClient
    from bitcoin_exchange import BitcoinExchange
    client = BitcoinClient()
    exchange = BitcoinExchange()
    # TODO: Don't just blindly query for email here... should only display logged-in buyer account info
    buyerEmail = db(db.buyer.id==request.vars.buyerId).select()[0].email
    # TODO: Create a brand new address so we can track the buyer instead of using the general-purpose "getaccountaddress"
    address = client.getaccountaddress(account=str(auth.user.id))
    # TODO: Move account creation into auth_user creation code when available and refactor this to query for accountId
    accountId = db.userBtcAccount.insert(
        auth_user_id=auth.user.id,
        accountName=auth.user.id,
        name=auth.user.id,
        description=auth.user.id,
        isDefault=True,
        isAutoExchanged=True)
    addressId = db.userBtcAddress.insert(
        userBtcAccount_id=accountId,
        address=address)
    exchangeRate = exchange.getlastprice()
    product = db(db.merchantProduct.id==request.vars.productId).select()[0]
    # btcTransactionId = db.btcTransaction.insert(
    #     btcTransactionType_id="""TODO""",
    #     transactionStatus_id="""TODO""",
    #     transactionId="""TODO""",
    #     sourceAddress="""TODO""",
    #     destinationAddress="""TODO""",
    #     isConfirmed="""TODO""",
    #     isIncoming="""TODO""")
    # # TODO: Take buyer information and insert into buyer table before insertion here
    # btcTransactionMerchantId = db.btcTransactionMerchant.insert(
    #     btcTransaction_id=btcTransactionId,
    #     buyer_id="""TODO""",
    #     productName=product.name,
    #     productDescription=product.description,
    #     quantity="""TODO""",
    #     pricePer=product.priceUSD,
    #     shippingCost=product.shippingCost,
    #     totalExpected=productPriceBTC,
    #     amountReceived="""TODO""",
    #     isRefunded="""TODO""")
    return dict(
        buyerEmail=buyerEmail,
        address=address, 
        accountId=accountId, 
        addressId=addressId, 
        exchangeRate=exchangeRate, 
        productName=product.name,
        productDescription=product.description,
        productPriceUSD=product.priceUSD, 
        productShippingCost=product.shippingCost,
        productPriceBTC=(product.priceUSD + product.shippingCost) / float(exchangeRate))
