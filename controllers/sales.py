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
        links=[lambda row: A(T('Purchase'),_href=URL("sales","purchaseProduct",args=[row.id]))],
        links_in_grid=True,
        user_signature=True,
        csv=False,
        headers={
            'merchantProduct.name': 'Product Name',
            'merchantProduct.description': 'Description',
            'merchantProduct.priceUSD': 'Price (USD)'})
    grid.element('.web2py_counter', replace=None)
    return dict(grid=grid)

def purchaseProduct():
    """
    TODO: should perform the following functions:
    1. Generate new bitcoin address
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
    return dict(message="TODO")