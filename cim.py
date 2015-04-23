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

    def get_instances_list(self, class_name):
        '''
        Get all instances of a class.

        returns: list with all instances as dictionaries.
        '''
        return [dict(x.items()) for x in self.session.EnumerateInstances(class_name)]

    def get_class_list(self):
        '''
        Get all names of classes available on the remote system.

        returns: list of class names as strings.
        '''
        return [x.classname for x in self.session.EnumerateClasses()]

    def get_what_we_want(self):
        '''
        Get all the information needed for the assignment.

        returns: string with os version information and a list with dictionaries with interface information.
        '''
        interfaces = self.get_instances_list("CIM_IPProtocolEndpoint")
        os = self.get_instances_list("CIM_OperatingSystem")
        
        data = [{"name": x['ElementName'], "ip": x['IPv4Address'], "mask": x['SubnetMask']} for x in interfaces]

        return os[0]["Version"], data
