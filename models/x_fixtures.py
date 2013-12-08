"""
BitBuddy fixtures (seed data).

Defines all required seed data to be populated into database on first run.
Includes test user accounts, global variables, business logic requirements,
administrative settings, and ID/description pairs for lookup tables.

More info: http://thadeusb.com/weblog/2010/4/21/using_fixtures_in_web2py

Author: Henry Nguyen (henry@bitbuddy.biz)
        Peter Lecki (peter@bitbuddy.biz)
"""

# Set "RESET = True" to reset ALL database data
# Useful for dev/testing... don't let this anywhere near production
RESET = False

if RESET:
    for table in db.tables():
        db[table].drop()
    db.commit()

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
# auth.add_permission('merchant', 'create_product', db.Product, 0)
# auth.add_permission('merchant', 'read_product', db.Product, 0)
# auth.add_permission('merchant', 'update_product', db.Product, 0)
# auth.add_permission('merchant', 'delete_product', db.Product, 0)

##
## Real seed data needed for all environments, including production.
##

if db(db.global_settings.id > 0).count() == 0:
    db.global_settings.insert(
        btc_from_buyer_ttl=180,
        min_transaction_confirmations=6,
        max_batch_wait_time=60
        )

if db(db.user_status.id > 0).count() == 0:
    db.user_status.insert(description='active')
    db.user_status.insert(description='disabled')
    db.user_status.insert(description='suspended')
    db.user_status.insert(description='deleted')

if db(db.phone_type.id > 0).count() == 0:
    db.phone_type.insert(description='Home')
    db.phone_type.insert(description='Office')
    db.phone_type.insert(description='Mobile')
    db.phone_type.insert(description='Fax')
    db.phone_type.insert(description='Other')

if db(db.btc_transaction_status.id > 0).count() == 0:
    # for all types
    db.btc_transaction_status.insert(description='confirmed')
    db.btc_transaction_status.insert(description='invalid')
    db.btc_transaction_status.insert(description='sent')
    # for type: merchant
    db.btc_transaction_status.insert(description='not_broadcast')
    db.btc_transaction_status.insert(description='received_full')
    db.btc_transaction_status.insert(description='received_short')
    db.btc_transaction_status.insert(description='received_over')
    db.btc_transaction_status.insert(description='received_full_late')
    db.btc_transaction_status.insert(description='received_short_late')
    db.btc_transaction_status.insert(description='received_over_late')
    db.btc_transaction_status.insert(description='expired')

if db(db.physical_address_type.id > 0).count() == 0:
    db.physical_address_type.insert(description='Billing')
    db.physical_address_type.insert(description='Shipping')
    db.physical_address_type.insert(description='Both')

if db(db.btc_transaction_type.id > 0).count() == 0:
    db.btc_transaction_type.insert(description='generic')
    db.btc_transaction_type.insert(description='exchange')
    db.btc_transaction_type.insert(description='merchant')
    db.btc_transaction_type.insert(description='refund')

if db(db.request_type.id > 0).count() == 0:
    db.request_type.insert(description='order')
    db.request_type.insert(description='withdraw')

if db(db.order_type.id > 0).count() == 0:
    db.order_type.insert(description='buy')
    db.order_type.insert(description='sell')


##
## Seed data for testing/QA only. In production, most of this should be entered
## using appadmin or some other UI like that. The rest should be entered 
## programmatically by our code.
##
