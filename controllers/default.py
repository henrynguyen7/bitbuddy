"""
Controller for /default service.

Provides most of the functionality for non-logged-in users, including
registration.

Some notes:
- index is the default action of any application
- user is required for authentication and authorization
- download is for downloading files uploaded in the db (does streaming)
- call exposes all registered services (none by default)

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

# -*- coding: utf-8 -*-

from bitcoin_client import BitcoinClient
from bitcoin_exchange import BitcoinExchange

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=None)

def user():
    return dict(form=auth())

def main():
    client = BitcoinClient()
    exchange = BitcoinExchange()
    blockcount = client.getblockcount()
    difficulty = client.getdifficulty()
    lastPrice = exchange.getlastprice()
    return dict(blockcount=blockcount, difficulty=difficulty, lastPrice=lastPrice)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
