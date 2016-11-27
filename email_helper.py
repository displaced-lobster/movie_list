#!/usr/bin/env python3
#-----------------------------------------------------------------------------------
# email_helper.py
# v1.0
# by Richard Mills
# Helps with send email functions
#-----------------------------------------------------------------------------------
import shelve

def store_login(filename):
    d = shelve.open(filename)
    d['from_address'] = input("From email address: ").lower()
    d['password'] = input("Password: ")
    d.close()
    return

def modify_to_addresses(filename, addresses, action):
    d = shelve.open(filename)

    if action == 'add':
        if 'to_addresses' not in d:
            d['to_addresses'] = []
        d['to_addresses'] += addresses
    #### This does not work vvvvv
    elif action == 'delete':
        for address in addresses:
            d['to_addresses'].remove(address)
    else:
        print('Usage: modify_to_addresses(filename, addresses, action)')
        print('addresses is a list of strings')
        print('action is "add" or "delete"')

    d.close()
    return
