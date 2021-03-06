"""
Model file for database setup and configuration.

Loads required resources for connecting to MySQL database
and defines basic structure and relationship of auth tables.
Also sets up SMTP mail settings.

Note: All files in models folder are loaded alphabetically, so order matters.

## TODO: Move SMTP settings out to a separate config file.

Author: Henry Nguyen (henry@bitbuddy.biz)
		Peter Lecki (peter@bitbuddy.biz)
"""

# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import json
import os

# Runs all modules with the latest changes instead of cached version, useful for dev
from gluon.custom_import import track_changes
track_changes(True)

# Necessary to allow CORS
if request.env.http_origin:
    response.headers['Access-Control-Allow-Origin'] = request.env.http_origin

# load mysql login credentials from resource file
resource_file = os.path.join(request.folder, "private", "resources.json")
with open(resource_file) as resource:
    resource_data = json.load(resource)

# TODO: Put these into a dict or some other Python data struct for this kinda thing
mysql_username = resource_data["mysql"]["username"]
mysql_password = resource_data["mysql"]["password"]
mysql_database = resource_data["mysql"]["database"]
mysql_host = resource_data["mysql"]["host"]
mysql_port = resource_data["mysql"]["port"]

# Use during normal runtime
db = DAL('mysql://' + mysql_username + ':' + mysql_password + '@' + mysql_host + '/' + mysql_database, pool_size=3, check_reserved=['mysql'], migrate=False)
# Use to rebuild/update schema
#db = DAL('mysql://' + mysql_username + ':' + mysql_password + '@' + mysql_host + '/' + mysql_database, pool_size=3, check_reserved=['mysql'])
# Use during normal runtime if schema updates are desired
#db = DAL('mysql://' + mysql_username + ':' + mysql_password + '@' + mysql_host + '/' + mysql_database, pool_size=3, check_reserved=['mysql'], lazy_tables=True)
# The migrate=False parameter prevents automatic modification of schema if it differs from its definition here. Schema mods should be done deliberately and manually.
# With lazy_tables=True, tables will be created only when accessed, which speeds up the code.
# Resulting connection string can be shown using: print db._uri

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
    #Field('user_status_id', 'reference user_status', notnull=True, ondelete='NO ACTION', readable=False, writable=False),
    Field('last_login_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('create_date', 'datetime', notnull=True, default=request.now, readable=False, writable=False),
    Field('update_date', 'datetime', notnull=True, default=request.now, update=request.now, readable=False, writable=False)]

#db.auth_user.user_status_id.requires = IS_IN_DB(db, user_status.id)

## create all tables needed by auth if not custom tables
# username=False specifies that email is used for login, not username.
auth.define_tables(username=False, signature=False)

# TODO: Verify links for everything below
auth.settings.password_min_length = 8
auth.settings.create_user_groups = False
auth.settings.login_next = URL('dashboard', 'index')
auth.settings.logout_next = URL('index')
auth.settings.profile_next = URL('index')
# TODO: After enabling email verification, redirect user to a page with instructions to check their email and click on the link to log in
auth.settings.register_next = URL('user', args='login')
auth.settings.retrieve_username_next = URL('index')
auth.settings.retrieve_password_next = URL('index')
auth.settings.change_password_next = URL('index')
auth.settings.request_reset_password_next = URL('user', args='login')
auth.settings.reset_password_next = URL('user', args='login')
auth.settings.verify_email_next = URL('user', args='login')

# TODO: Change to true to require email verification before account is created
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.messages.verify_email = 'Click on the link http://' + request.env.http_host + URL(r=request,c='default',f='user',args=['verify_email']) + '/%(key)s to verify your email'
auth.messages.reset_password = 'Click on the link http://' + request.env.http_host + URL(r=request,c='default',f='user',args=['reset_password']) + '/%(key)s to reset your password'

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
