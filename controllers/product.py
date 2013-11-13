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

def product():
    form = SQLFORM(db.merchantProduct, 
        fields=['name', 'merchantNumber', 'description', 'priceUSD', 'shippingCost'],
        labels={
            'name': 'Product Name',
            'merchantNumber': 'Merchant ID Number',
            'description': 'Description',
            'priceUSD': 'Price in USD',
            'shippingCost': 'Shipping Cost'
        },
        deletable=True)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    # records = db.merchantProduct()
    records = SQLFORM.grid(db.merchantProduct, 
        fields=['name', 'merchantNumber', 'description', 'priceUSD', 'shippingCost'],
        headers={
            'name': 'Product Name',
            'merchantNumber': 'Merchant ID Number',
            'description': 'Description',
            'priceUSD': 'Price in USD',
            'shippingCost': 'Shipping Cost'
        })
    return dict(form=form, records=records)
    # return dict(form=crud.update(db.merchantProduct), records=records)