#!/bin/bash
sudo /Library/StartupItems/MySQLCOM/MySQLCOM start &
bitcoind &
Python /Users/henry/dev/web2py/web2py.py
