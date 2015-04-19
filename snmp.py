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

    def get_bulk_OID_name_value(self, oid, depth):
        '''
        Get a name, value pair from a OID

        returns: name, value
        '''
        errorIndication, errorStatus, errorIndex, varBindTable = self.cmd.bulkCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.address, self.port)),
            0, depth,
            oid
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                #print varBindTable

                data = []

                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        data.append(("%s" % name.prettyPrint(), "%s" % val.prettyPrint()))
                return data

    #def get_bulk_OID_name_value(self, oidlist):
    #    '''
    #    Get a dictionary with names as keys and value as value

    #    returns: { OID: value }
    #    '''
    #    result = {}
    #    for oid in oidlist:
    #        name, value = self.get_OID_name_value(oid)
    #        result[name] = value
    #    return result


    def get_what_we_want(self):
        ipaddress = "1.3.6.1.2.1.4.20.1.1"
        mask = "1.3.6.1.2.1.4.20.1.3"
        ifname = "1.3.6.1.2.1.2.2.1.2"

        _, number_of_interfaces = self.get_OID_name_value("1.3.6.1.2.1.2.1.0")
        _, os = self.get_OID_name_value("1.3.6.1.2.1.1.1.0")

        ipaddresses = self.get_bulk_OID_name_value(ipaddress, 1)
        masks = self.get_bulk_OID_name_value(mask, 1)
        ifnames = self.get_bulk_OID_name_value(ifname, 1)

        data = []

        for i in range(int(number_of_interfaces)):
            data.append({
                "name": ifnames[i][1],
                "ip": ipaddresses[i][1],
                "mask": masks[i][1],
            })

        return os, data


