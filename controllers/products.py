"""
Controller for /product service.

Handles all product-related methods such as product creation,
reading, updates, and deletion.

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

from gluon.custom_import import track_changes
from gluon.tools import Crud

# Runs all modules with the latest changes instead of cached version, useful for dev
track_changes(True)

crud = Crud(db)

@request.restful()
def api():
    response.view = 'generic.json'
    def GET(id):
        return dict(person = db.product(id))
    def POST(**fields):
        return db.product.validate_and_insert(**fields)
    return locals()

def products():
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
    grid.element('.web2py_counter', replace=None)
    return dict(grid=grid)
