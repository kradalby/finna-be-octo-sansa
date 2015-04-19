#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: app.py
Author: Kristoffer Dalby, Tor Håkon Bonsaksen, Trond Walleraunet
Description: Main web app
'''

from flask import Flask, render_template
from cim import Cimom
from snmp import SNMP

cim_url = "http://ttm4128.item.ntnu.no:5988"
c = Cimom(cim_url)
s = SNMP("vsop.online.ntnu.no", 161, "public")


app = Flask(__name__)

@app.route('/')
def index():
#    server_os = "Windows 98 enterprise server"
#    interfaces = [
#        {"name": "test1", "ip": "91.2.34.198", "mask": "255.255.255.0"}, 
#        {"name": "test2", "ip": "91.2.34.197", "mask": "255.255.255.0"}]
    server_os, interfaces = c.getWhatWeNeed()
    return render_template('index.html', interfaces=interfaces, server_os=server_os, cim=True)


@app.route('/snmp/')
def snmp():
    #server_os = "Debian 3.14"
    #interfaces = [
    #    {"name": "test3", "ip": "91.2.34.198", "mask": "255.255.255.0"}, 
    #    {"name": "test4", "ip": "91.2.34.197", "mask": "255.255.255.0"}]
    server_os, interfaces = s.get_what_we_want()
    return render_template('index.html', interfaces=interfaces, server_os=server_os, cim=False)

if __name__ == '__main__':
    app.debug = True
    app.run()
