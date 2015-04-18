#!/usr/bin/env python
'''
File: cim.py
Author: Kristoffer Dalby
Description: CIM functionality
'''

import requests
import pywbem
from pprint import pprint

class Cimom():
    
    def __init__(self, url):
        self.url = url
        self.session = pywbem.WBEMConnection(self.url)

    def getInstacesList(self, class_name):
        '''
        Get all instances of a class.

        returns: list with all instances as dicts
        '''
        return [dict(x.items()) for x in self.session.EnumerateInstances(class_name)]

    def getClassList(self):
        '''
        Get all names of classes available

        returns: list of class names
        '''
        return [x.classname for x in self.session.EnumerateClasses()]




