#!/usr/bin/env python
'''
File: snmp.py
Author: Kristoffer Dalby
Description: SNMP functionality
'''

import requests
#import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pprint import pprint

class SNMP():
    
    def __init__(self, address, port, community):
        self.address = address
        self.port = port
        self.community = community

        self.cmd = cmdgen.CommandGenerator()

    def get_OID_name_value(self, oid):
        '''
        Get a name, value pair from a OID

        returns: name, value
        '''
        errorIndication, errorStatus, errorIndex, varBinds = self.cmd.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.address, self.port)),
            oid
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    return "%s" % name.prettyPrint(), "%s" % val.prettyPrint()

    def get_bulk_OID_name_value(self, oidlist):
        '''
        Get a dictionary with names as keys and value as value

        returns: { OID: value }
        '''
        result = {}
        for oid in oidlist:
            name, value = self.get_OID_name_value(oid)
            result[name] = value
        return result




