"""

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

from gluon.custom_import import track_changes
from gluon.tools import Crud

# Runs all modules with the latest changes instead of cached version, useful for dev
track_changes(True)

crud = Crud(db)

def wallet():
    # TODO: Set these attributes directly on db table definitions... remove from here when schema.py is completed
    db.product.id.writable = False
    db.product.id.readable = False
    db.product.auth_user_id.writable = False
    db.product.auth_user_id.readable = False
    db.product.price_btc.writable = False
    db.product.price_btc.readable = False
    db.product.create_date.writable = False
    db.product.create_date.readable = False
    grid = SQLFORM.grid(
        query=db.product.auth_user_id==request.vars.auth_user_id,
        fields=[
            db.product.name,
            db.product.number,
            db.product.description,
            db.product.price_usd,
            db.product.shipping_cost],
        deletable=True,
        editable=True,
        details=False,
        selectable=None,
        searchable=False,
        links=None,
        links_in_grid=False,
        user_signature=False,
        csv=False,
        headers={
            'product.name': 'Product Name',
            'product.number': 'Merchant ID Number',
            'product.description': 'Description',
            'product.price_usd': 'Price (USD)',
            'product.shipping_cost': 'Shipping Cost'})
    return dict(grid=grid)
