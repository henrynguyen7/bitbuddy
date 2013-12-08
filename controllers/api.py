"""
Controller for /api

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

from gluon.custom_import import track_changes
from gluon.tools import Crud

# Runs all modules with the latest changes instead of cached version, useful for dev
track_changes(True)

crud = Crud(db)

@request.restful()
def product():
    response.view = 'generic.json'
    def GET(id):
        return dict(person = db.product(id))
    def POST(**fields):
        return db.product.validate_and_insert(**fields)
    return locals()
