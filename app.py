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
import re

cim_url = "http://ttm4128.item.ntnu.no:5988"

# Initialize the Cimom class
c = Cimom(cim_url)

# Initialize the SNMP class
s = SNMP("vsop.online.ntnu.no", 161, "public")

# Initialize the Flask framwork
app = Flask(__name__)

# Flask uses the route method to map out what each part of the web address will call in our system.
# This spesific on maps the root of the webserver to the CIM view of the application.
@app.route('/')
def index():
    
    # Use the Cimom class to query and get the information we want from the host.
    server_os, interfaces = c.get_what_we_want()

    # Use regex to get the "Pretty Name" from the version string. This only displays the OS name and the version.
    match = re.search("(?<=PRETTY_NAME=)\"(.*?)\"", server_os)
    if match.group(0):
        server_os = match.group(0)

    # Render the template with the information we got.
    return render_template('index.html', interfaces=interfaces, server_os=server_os, cim=True)


@app.route('/snmp/')
def snmp():

    # Use the SNMP class to query and get the information we want from the host.
    server_os, interfaces = s.get_what_we_want()

    # Render the template with the information we got.
    return render_template('index.html', interfaces=interfaces, server_os=server_os, cim=False)

if __name__ == '__main__':
    app.debug = True
    app.run()
