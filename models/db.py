# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

from mysql_resources import mysqlUser, mysqlPassword, mysqlDatabase, mysqlPort, mysqlHost

db = DAL('mysql://' + mysqlUser + ':' + mysqlPassword + '@' + mysqlHost + '/' + mysqlDatabase, pool_size=1, check_reserved=['mysql'])

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
    Field('createDate','datetime', default=request.now)]

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## define groups
## example: auth.add_group('admin', 'admin')
auth.add_group('admin', 'admin')
auth.add_group('user', 'user')
auth.add_group('merchant', 'merchant')
auth.add_group('buyer', 'buyer')

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
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)