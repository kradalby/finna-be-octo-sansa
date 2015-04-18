#!/usr/bin/env python
'''
File: app.py
Author: Kristoffer Dalby, Tor Håkon Bonsaksen, Trond Walleraunet
Description: Main web app
'''

from flask import Flask, render_template
from cim import Cimom
from snmp import SNMP

cim_url = "http://ttm4128.item.ntnu.no:5988"
c = Cimom(url)
s = SNMP("vsop.online.ntnu.no", 161, "public")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', servers=servers)

if __name__ == '__main__':
    app.debug = True
    app.run()
