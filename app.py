#!/usr/bin/env python
'''
File: app.py
Author: Kristoffer Dalby, Tor Håkon Bonsaksen, Trond Walleraunet
Description: Main web app
'''

cim_url = "http://ttm4128.item.ntnu.no:5988"

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', servers=servers)

if __name__ == '__main__':
    app.debug = True
    app.run()
