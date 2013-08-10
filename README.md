# BitBuddy is a web server written in Python using the web2py framework to facilitate easy merchant acceptance of Bitcoins.

# DEPENDENCIES:
- bitcoind: https://github.com/bitcoin/bitcoin
- bitcoinrpc: https://github.com/jgarzik/python-bitcoinrpc

# INSTALLATION:
- 1) Install web2py: http://www.web2py.com/init/default/download. It is recommended to install from source as the Mac OS X client has errors on startup.
- 2) Clone this project into the web2py/applications/ folder. The name given to the folder will be the name of the web2py project, meaning all request URLs will include that name. It is therefore recommended to keep this name simple, e.g. "bitbuddy".

# CODE NOTES:
- In Python, every function call to an object function passes a copy of "self" as the first argument. From Python docs: "Often, the first argument of a method is called self. This is nothing more than a convention: the name self has absolutely no special meaning to Python. Note, however, that by not following the convention your code may be less readable to other Python programmers, and it is also conceivable that a class browser program might be written that relies upon such a convention."
- Every object has an __init__(self) method that can be overridden which will be called every time the object is instantiated.
- Seed data for the database is called "fixtures". More info: http://thadeusb.com/weblog/2010/4/21/using_fixtures_in_web2py
- "If you drop the entire db (not using web2py), you should delete all the /databases/*.table files -- there is one such file for each table containing metadata about that table (based on migrations done by web2py). If you make changes to the db from outside web2py, those files will no longer be consistent with the state of the db. When you drop the whole db, just delete those files." From: https://groups.google.com/forum/#!topic/web2py/d0Ztw80_JUY
