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
        query=db.product.auth_user_id==request.vars.auth_user_id,
        fields=[
            db.product.name,
            db.product.description,
            db.product.price_usd],
        deletable=False,
        editable=False,
        details=False,
        selectable=None,
        searchable=False,
        # Take user to create_buyer page first instead of directly to purchase_product page. TODO: allow login if already existing.
        # links=[lambda row: A(T('Purchase'),_href=URL("sales","purchaseProduct",vars={'product_id': row.id}))],
        links=[lambda row: A(T('Purchase'),_href=URL("sales","createBuyerAccount",vars=dict(product_id=row.id)))],
        links_in_grid=True,
        user_signature=True,
        csv=False,
        headers={
            'product.name': 'Product Name',
            'product.description': 'Description',
            'product.price_usd': 'Price (USD)'})
    grid.element('.web2py_counter', replace=None)
    return dict(grid=grid)

def create_buyer_account():
    # TODO: modify to create a new auth_user of type "buyer" instead of inputting an entry directly into the buyer table.
    form = SQLFORM(db.buyer)
    if form.process().accepted:
        redirect(URL('purchase_product', vars=dict(buyer_id=form.vars.id, product_id=request.vars.product_id)))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def purchase_product():
    """
    TODO: should perform the following functions:
    1. Generate new bitcoin address
    1a. Add bitcoin address and account to user_btc_address and user_btc_account tables
    2. Query exchange for latest exchange rate
    3. Calculate price_btc of Product
    4. Display popup page with:
        - 10 minute timer
        - product info
        - price_btc
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
    buyer_email = db(db.buyer.id==request.vars.buyer_id).select()[0].email
    # TODO: Create a brand new address so we can track the buyer instead of using the general-purpose "getaccountaddress"
    address = client.getaccountaddress(account=str(auth.user.id))
    # TODO: Move account creation into auth_user creation code when available and refactor this to query for account_id
    account_id = db.user_btc_account.insert(
        auth_user_id=auth.user.id,
        account_name=auth.user.id,
        name=auth.user.id,
        description=auth.user.id,
        is_default=True,
        is_auto_exchanged=True)
    address_id = db.user_btc_address.insert(
        user_btc_account_id=account_id,
        address=address)
    exchange_rate = exchange.getlastprice()
    product = db(db.product.id==request.vars.product_id).select()[0]
    # btc_transaction_id = db.btc_transaction.insert(
    #     btc_transaction_type_id="""TODO""",
    #     transaction_status_id="""TODO""",
    #     transaction_id="""TODO""",
    #     source_address="""TODO""",
    #     destination_address="""TODO""",
    #     is_confirmed="""TODO""",
    #     is_incoming="""TODO""")
    # # TODO: Take buyer information and insert into buyer table before insertion here
    # btc_transaction_merchant_id = db.btc_transaction_merchant.insert(
    #     btc_transaction_id=btc_transaction_id,
    #     buyer_id="""TODO""",
    #     product_name=product.name,
    #     product_description=product.description,
    #     quantity="""TODO""",
    #     price_per=product.price_usd,
    #     shipping_cost=product.shipping_cost,
    #     total_expected=product_price_btc,
    #     amount_received="""TODO""",
    #     is_refunded="""TODO""")
    return dict(
        buyer_email=buyer_email,
        address=address, 
        account_id=account_id, 
        address_id=address_id, 
        exchange_rate=exchange_rate, 
        product_name=product.name,
        product_description=product.description,
        product_price_usd=product.price_usd, 
        product_shipping_cost=product.shipping_cost,
        product_price_btc=(product.price_usd + product.shipping_cost) / float(exchange_rate))
