"""
Model file for database setup and configuration.

Loads required resources for connecting to MySQL database
and defines basic structure and relationship of auth tables.
Also sets up SMTP mail settings.

Note: All files in models folder are loaded alphabetically, so order matters.

## TODO: Move SMTP settings out to a separate config file.

Author: Henry Nguyen (henry@bitbuddy.biz)
"""

# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import json
import os

# Necessary to allow CORS
if request.env.http_origin:
    response.headers['Access-Control-Allow-Origin'] = request.env.http_origin
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = 86400

    if request.env.request_method == 'OPTIONS':
        if request.env.http_access_control_request_method:
            print request.env.http_access_control_request_method
            response.headers['Access-Control-Allow-Methods'] = request.env.http_access_control_request_method
            if request.env.http_access_control_request_headers:
                response.headers['Access-Control-Allow-Headers'] = request.env.http_access_control_request_headers

# load mysql login credentials from resource file
resourceFile = os.path.join(request.folder, "private", "resources.json")
resource = open(resourceFile, 'r')
resourceData = json.load(resource)
resource.close()

# TODO: Put these into a dict or some other Python data struct for this kinda thing
mysqlUsername = resourceData["mysql"]["username"]
mysqlPassword = resourceData["mysql"]["password"]
mysqlDatabase = resourceData["mysql"]["database"]
mysqlHost = resourceData["mysql"]["host"]
mysqlPort = resourceData["mysql"]["port"]

db = DAL('mysql://' + mysqlUsername + ':' + mysqlPassword + '@' + mysqlHost + '/' + mysqlDatabase, pool_size=1, check_reserved=['mysql'])

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## define extra fields for auth_* tables
auth.settings.extra_fields['auth_user'] = [
    Field('isActive', 'boolean', default=True),
    Field('firstName'),
    Field('lastName'),
    Field('company'),
    Field('website'),
    Field('lastLoginDate'),
    Field('createDate', 'datetime', default=request.now)]

## create all tables needed by auth if not custom tables
# username=false specifies that username is not required and will instead use email for login
auth.define_tables(username=False, signature=False)

## add groups only if they don't already exist
def add_group_if_not_exists(group, description):
    if not db(db.auth_group.role==group).count():
        auth.add_group(group, description)

add_group_if_not_exists('admin', 'admin')
add_group_if_not_exists('user', 'user')
add_group_if_not_exists('merchant', 'merchant')
add_group_if_not_exists('buyer', 'buyer')

## define permissions for groups
## example: auth.add_permission(group_id, 'name', 'object', record_id)
# TODO: Determine how to add permission when table not defined yet (due to lazy instantiation)
# TODO: Determine how to allow permissions on only records that belong to that user
# auth.add_permission('merchant', 'createProduct', db.Product, 0)
# auth.add_permission('merchant', 'readProduct', db.Product, 0)
# auth.add_permission('merchant', 'updateProduct', db.Product, 0)
# auth.add_permission('merchant', 'deleteProduct', db.Product, 0)

## configure email
mail = auth.settings.mailer
## TODO: Modify for BitBuddy SMTP
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'admin@bitbuddy.biz'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)