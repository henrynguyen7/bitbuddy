"""
Controller for /product service.

Handles all product-related methods such as product creation,
reading, updates, and deletion.

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

# Runs all modules with the latest changes instead of cached version, useful for dev
from gluon.custom_import import track_changes
track_changes(True)

@request.restful()
def product():
    response.view = 'generic.json'
    response.headers['Access-Control-Allow-Origin'] = "*"
    def GET(tablename,id):
        if not tablename=='merchantProduct': raise HTTP(400)
        return dict(person = db.merchantProduct(id))
    def POST(tablename,**fields):
        if not tablename=='merchantProduct': raise HTTP(400)
        return db.person.validate_and_insert(**fields)
    def PUT(*args,**vars):
        return dict()
    def DELETE(*args,**vars):
        return dict()
    return locals()