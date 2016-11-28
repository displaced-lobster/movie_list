#!/usr/bin/env python3
#-----------------------------------------------------------------------------------
# email_helper.py
# v1.0
# by Richard Mills
# Helps with send email functions
#-----------------------------------------------------------------------------------
import shelve
import re

email_pat = re.compile('^([a-z0-9+_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,24})$')

def store_login(filename):
    d = shelve.open(filename)
    d['from_address'] = input("From email address: ").lower()
    if re.fullmatch(email_pat, d['from_address']) == None:
        print('Not an email!')
        d.close()
        return
    d['password'] = input("Password: ")
    d.close()
    return

def modify_to_addresses(filename, addresses, action):
    d = shelve.open(filename)

    if action == 'add':
        if 'to_addresses' not in d:
            d['to_addresses'] = []

        failed = []
        temp = []

        for address in addresses:
            if re.fullmatch(email_pat, address) != None:
                temp.append(address)
            else:
                failed.append(address)

        d['to_addresses'] += temp

        if len(failed) > 0:
            print('The following emails are incorrect:')
            for fail in failed:
                print('\t', fail)

    elif action == 'delete':
        temp = d['to_addresses']
        for address in addresses:
            temp.remove(address)
        d['to_addresses'] = temp
        
    else:
        print('Usage: modify_to_addresses(filename, addresses, action)')
        print('addresses is a list of strings')
        print('action is "add" or "delete"')

    d.close()
    return
