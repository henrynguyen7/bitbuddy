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
        return dict(person = db.merchantProduct(id))
    def POST(**fields):
        return db.merchantProduct.validate_and_insert(**fields)
    return locals()

def products():
    # TODO: Set these attributes directly on db table definitions... remove from here when schema.py is completed
    db.merchantProduct.id.writable = False
    db.merchantProduct.id.readable = False
    db.merchantProduct.auth_user_id.writable = False
    db.merchantProduct.auth_user_id.readable = False
    db.merchantProduct.priceBTC.writable = False
    db.merchantProduct.priceBTC.readable = False
    db.merchantProduct.createDate.writable = False
    db.merchantProduct.createDate.readable = False
    grid = SQLFORM.grid(
        query=db.merchantProduct.auth_user_id==request.vars.auth_user_id,
        fields=[
            db.merchantProduct.name,
            db.merchantProduct.merchantNumber,
            db.merchantProduct.description,
            db.merchantProduct.priceUSD,
            db.merchantProduct.shippingCost],
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
            'merchantProduct.name': 'Product Name',
            'merchantProduct.merchantNumber': 'Merchant ID Number',
            'merchantProduct.description': 'Description',
            'merchantProduct.priceUSD': 'Price (USD)',
            'merchantProduct.shippingCost': 'Shipping Cost'})
    return dict(grid=grid)